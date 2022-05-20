import asyncio
import re
from urllib.parse import urlparse

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from novels.api.serializers import (
    NovelServiceSerializer,
    ResourceSerializer,
    ResourceFullSerializer,
    SearchIncomeSerializer,
    ResourceFromUrlIncomeSerializer,
    TitleIncomeSerializer,
    AuthorIncomeSerializer,
    SearchPageSerializer,
    ChapterIncomeSerializer,
    SiteLanguageSerializer,
    ChapterListIncomeSerializer,
)
from novels.utils import prepare_services_response
from novels.scripts.novel import get_resource_data
from parsers.models import NovelParser, Resource, SiteLanguage
from translate.utils import run_async2
from utils.browser import (
    prepare_browser, return_running, get_browser_pages
)


class NovelServiceAPIView(APIView):
    def get(self, request):
        queryset = NovelParser.objects.all()
        data = NovelServiceSerializer(
            queryset, 
            context={'request': request}, 
            many=True
        ).data
        return Response(
            prepare_services_response(data),
            status=status.HTTP_200_OK
        )


class SiteLanguageAPIView(APIView):
    def get(self, request):
        queryset = SiteLanguage.objects.all()
        data = SiteLanguageSerializer(
            queryset, 
            context={'request': request}, 
            many=True
        ).data
        return Response(data, status=status.HTTP_200_OK)


class ResourceListAPIView(APIView):
    def get_novel_parser(self, lang_code, service):
        return get_object_or_404(
            NovelParser,
            main_language__code=lang_code,
            slug=service
        )

    def get(self, request, lang_code, service):
        novel_parser = self.get_novel_parser(lang_code, service)
        queryset = novel_parser.resource_set.all()
        data = ResourceSerializer(queryset, many=True).data
        return Response(data, status=status.HTTP_200_OK)


class ResourceAPIView(APIView):
    serializer_classes = {
        'search_page': {
            'validate_income': SearchIncomeSerializer,
            'data_serializer': SearchPageSerializer,
        },
        'novel_page': {
            'validate_income': TitleIncomeSerializer,
            'data_serializer': ResourceFullSerializer,
        },
        'author_page': {
            'validate_income': AuthorIncomeSerializer,
            'data_serializer': ResourceFullSerializer,
        },
        'chapter_page': {
            'validate_income': ChapterIncomeSerializer,
            'data_serializer': ResourceFullSerializer,
        },
        'chapter_list_page': {
            'validate_income': ChapterListIncomeSerializer,
            'data_serializer': ResourceFullSerializer,
        },
    }

    def get_income_serializer_class(self, resource_name):
        return self.serializer_classes[resource_name]['validate_income']

    def get_data_serializer_class(self, resource_name):
        return self.serializer_classes[resource_name]['data_serializer']

    def get_resource(self, lang_code, service, resource_name):
        return get_object_or_404(
            Resource,
            name=resource_name,
            novel_parser__slug=service,
            novel_parser__main_language__code=lang_code,
        )

    def get(self, request, lang_code, service, resource_name):
        resource = self.get_resource(lang_code, service, resource_name)
        data = ResourceFullSerializer(resource).data
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, lang_code, service, resource_name, url=None):
        # validate income
        serializer_class = self.get_income_serializer_class(resource_name)
        print(serializer_class)
        serializer = serializer_class(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        income_data = serializer.validated_data

        resource = self.get_resource(lang_code, service, resource_name)
        data_serializer_class = self.get_data_serializer_class(resource_name)
        resource_data = data_serializer_class(resource).data
        browser, page = prepare_browser(
            service, resource_data.get('page'), type='Novel')

        result = asyncio.run(run_async2(
            get_resource_data,
            page_index=page.index,
            browser_endpoint=browser.wsEndpoint,
            lang_code=lang_code,
            url=url or resource.novel_parser.url,
            request=request,
            query_params={
                'lang_code': lang_code,
                'service': service,
                'resource_name': resource_name,
            },
            **resource_data,
            **income_data,
        ))

        page.in_use = False
        page.save()

        if 'exception' in result:
            raise result['exception']

        # print(result)

        return Response(result, status=status.HTTP_200_OK)


class ServiceMainPageAPIView(APIView):
    def get_novel_parser(self, lang_code, service):
        return get_object_or_404(
            NovelParser,
            main_language__code=lang_code,
            slug=service
        )

    def get(self, request, lang_code, service):
        novel_parser = self.get_novel_parser(lang_code, service)
        search_page = novel_parser.resource_set.filter(
            name='search_page'
        ).first()
        search_data = ResourceFullSerializer(search_page).data
        data = {
            'search': search_data
        }
        return Response(data, status=status.HTTP_200_OK)


class ResourceFromUrlAPIView(APIView):
    def get_string_keys(self, string):
        from string import Formatter

        keys = [t[1] for t in Formatter().parse(string) if t[1] is not None]
        return keys

    def find_resource(self, url, lang_code, service):
        novel_parser = ServiceMainPageAPIView.get_novel_parser(
            self, lang_code, service
        )
        resources = novel_parser.resource_set.values(
            'urn_regex', 'name', 'urn')
        results = []
        for resource in resources:
            if not resource['urn_regex']:
                continue
            find = re.findall(resource['urn_regex'], url)
            if find:
                keys = self.get_string_keys(resource['urn'])
                find = find[0] if isinstance(find[0], tuple) else find
                values = [x for x in find if x]
                keys.append('page_num') if len(values) == 3 else ''
                results.append((resource['name'], dict(zip(keys, values))))
        if results:
            return max(results, key=lambda x: len(x[1]))
        return None, None

    def post(self, request, lang_code, service):
        serializer = ResourceFromUrlIncomeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        url = serializer.validated_data['url']
        resource, data = self.find_resource(url, lang_code, service)
        print(data)
        if resource:
            if hasattr(request.data, '_mutable'):
                request.data._mutable = True
            request.data.update(data)
            res = ResourceAPIView()
            return res.post(
                request, lang_code, service, resource, url=url
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ExtResourceFromUrlAPIView(ResourceFromUrlAPIView):
    def search_lang_code_service(self, request, url: str):
        from math import ceil

        if 'http://' not in url and 'https://' not in url and not url.startswith('//'):
            url = 'http://' + url
        netloc = urlparse(url).netloc
        arr = netloc.split('.')
        host_name = arr[ceil(len(arr)/2) - 1]
        novel_parser = NovelParser.objects.filter(slug=host_name).first()
        if not novel_parser:
            return None, host_name
        lang_code = novel_parser.main_language.code
        return lang_code, host_name, url

    def post(self, request):
        serializer = ResourceFromUrlIncomeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        url = serializer.validated_data['url']
        lang_code, service, url = self.search_lang_code_service(request, url)
        if not (lang_code and service):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if hasattr(request.data, '_mutable'):
            request.data._mutable = True
        request.data.update({'url': url})
        return super().post(request, lang_code, service)