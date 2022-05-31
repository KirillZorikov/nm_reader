import asyncio

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from django.http import Http404

from parsers.models import Parser, Page
from parsers.api.serializers import (
    InitPagesSerializer,
    ServiceMaxPagesSerializer,
    ServiceTimeoutSerializer,
)
from utils.browser import get_browser, create_pages
from utils.async_ import run_async


@api_view(('POST',))
@permission_classes((AllowAny,))
def init_pages(request):
    # return Response(status=status.HTTP_200_OK)
    serializer = InitPagesSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    validated_data = serializer.validated_data
    service = validated_data['service_slug']
    parser_type = validated_data['type']

    if not validated_data.get('inited'):
        diff_count = validated_data['diff']
        browser = get_browser(parser_type, service)
        pages_index = create_pages(browser, service, diff_count)
    else:
        pages_index = list(Page.objects.annotate_parser_slug().filter(
            parser_slug=service
        ).values_list('page_id', flat=True))

    return Response(pages_index, status=status.HTTP_200_OK)


@api_view(('POST',))
@permission_classes((AllowAny,))
def set_service_pages_limit(request):
    serializer = ServiceMaxPagesSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    service_slug = serializer.validated_data['service_slug']
    pages_count = serializer.validated_data['pages_count']

    parser = Parser.objects.annotate_related_parser_slug().filter(
        related_parser_slug=service_slug
    ).first()
    if not parser:
        raise Http404
    parser.max_pages_count = pages_count
    parser.save()

    return Response(status=status.HTTP_200_OK)


@api_view(('POST',))
@permission_classes((AllowAny,))
def set_service_timeout(request):
    serializer = ServiceTimeoutSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    service_slug = serializer.validated_data['service_slug']
    timeout = serializer.validated_data['timeout']

    parser = Parser.objects.annotate_related_parser_slug().filter(
        related_parser_slug=service_slug
    ).first()
    if not parser:
        raise Http404
    parser.timeout = timeout
    parser.save()

    return Response(status=status.HTTP_200_OK)
