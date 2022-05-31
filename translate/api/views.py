import asyncio

from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
)
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from django.http import Http404
from pyppeteer.browser import Browser as PyppeteerBrowser

from translate.api.serializers import (
    TranslateParserDetailSerializer,
    TranslateParserListSerializer,
    TextTranslateSerializer,
    YandexCaptchaSerializer,
    ImageTranslateSerializer,
    ParserSerializer,
)
from translate.scripts.translate import translate, solve_captcha, translate_api
from translate.utils import run_async2, get_captcha_data
from parsers.models import Browser, Parser, Page, TranslateParser
from utils.browser import (
    prepare_browser, return_running, get_browser_pages
)
from utils.pyppeteer import get_pages_dict


class TranslateParserListAPIView(ListAPIView):
    pagination_class = None
    serializer_class = TranslateParserListSerializer
    queryset = TranslateParser.objects

    # def get_queryset(self):
    #     return TranslateParser.objects.annotate_related_parser_slug().filter(
    #         type='Translate'
    #     )


class TranslateParserRetrieveAPIView(RetrieveAPIView):
    serializer_class = TranslateParserDetailSerializer
    lookup_url_kwarg = 'service'

    def get_queryset(self):
        return TranslateParserListAPIView.get_queryset(self)

    def get_object(self):
        service = self.kwargs['service']
        queryset = self.get_queryset()
        obj = queryset.annotate_related_parser_slug().filter(
            related_parser_slug=service
        ).first()
        if not obj:
            raise Http404
        return obj


class TranslateAPIView(APIView):
    parser = None
    api_list = ['google_api']

    def is_api_service(self, service):
        if service.endswith('_api'):
            if service not in self.api_list:
                raise Http404
            return True

    def get_service(self, service):
        if self.is_api_service(service):
            return service[:-4]
        return service

    def set_parser(self, service):
        self.parser = Parser.objects.annotate_related_parser_slug().filter(
            related_parser_slug=service
        ).first()

    def get_parser(self, service):
        if not self.parser:
            self.set_parser(service)
        return self.parser

    def get_serializer_class(self, service):
        service = self.get_service(service)
        parser = self.get_parser(service)
        if parser.type == 'Translate':
            return TextTranslateSerializer
        elif parser.type == 'TranslateImage':
            return ImageTranslateSerializer

    def handle_api(self, service, data):
        result = asyncio.run(run_async2(
            translate_api,
            service=service,
            ** data
        ))
        if 'exception' in result:
            raise result['exception']
        return Response(
            result['data'], status=status.HTTP_200_OK
        )

    def post(self, request, service: str, format=None):

        # validate income data
        serializer_class = self.get_serializer_class(service)
        serializer = serializer_class(
            context={'slug': self.get_service(service)},
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        if self.is_api_service(service):
            return self.handle_api(service, validated_data)

        # prepare data to translate and lock page
        parser_data = ParserSerializer(instance=self.get_parser(service)).data
        browser, page = prepare_browser(
            service, 
            type='Translate',
            max_pages=parser_data['max_pages_count'],
        )
        result = asyncio.run(run_async2(
            translate,
            timeout=parser_data['timeout'],
            browser_endpoint=browser.wsEndpoint,
            browser_id=browser.pk,
            page_id=page.page_id,
            parser_data=parser_data,
            service=service,
            **validated_data
        ))

        # release page
        if not 'captcha' in result['message']:
            page.in_use = False
            page.save()
        if not result['success']:
            page.fails_count += 1
            page.save()
            raise result['exception']

        if 'data' not in result:
            print(result)

        translate_dict = dict(zip(validated_data['data'], result['data']))

        return Response(
            translate_dict, status=status.HTTP_200_OK
        )


@api_view(('POST',))
@permission_classes((AllowAny,))
def captcha_solve(request):

    # validate income data
    serializer = YandexCaptchaSerializer(
        data=request.data
    )
    serializer.is_valid(raise_exception=True)
    validated_data = serializer.validated_data

    captcha_parser_data = get_captcha_data(serializer.data['service_slug'])
    browser = Browser.objects.filter(pk=validated_data['browser_id']).first()
    result = asyncio.run(run_async2(
        solve_captcha,
        browser_endpoint=browser.wsEndpoint,
        page_id=validated_data['page_id'],
        solve=validated_data['solution'],
        captcha_parser_data=captcha_parser_data,
    ))

    return Response(
        result,
        status=200 if result['success'] else 400
    )


@api_view(('GET',))
@permission_classes((AllowAny,))
def pages_status(request):
    browser = Browser.objects.filter(type='Translate').first()
    running_browser = ''
    if browser:
        running_browser = asyncio.run(run_async2(
            return_running,
            endpoint=browser.wsEndpoint,
        ))
    if not isinstance(running_browser, PyppeteerBrowser):
        return Response(
            {'result': 'browser is not running'},
            status=status.HTTP_200_OK
        )
    pages = asyncio.run(run_async2(
        get_browser_pages,
        endpoint=browser.wsEndpoint
    ))
    pages = get_pages_dict(pages)
    services = {}
    for page in Page.objects.annotate_parser_slug().values(
        'parser_slug', 'page_id', 'in_use', 'fails_count', 'id'
    ):
        page_info = {
            'id': page['id'],
            'page_id': page['page_id'],
            'current_url': pages[page['page_id']].url,
            'in_use': page['in_use'],
            'fails_count': page['fails_count']
        }
        services.setdefault(page['parser_slug'], []).append(page_info)
    return Response(
        {'result': services},
        status=status.HTTP_200_OK
    )
