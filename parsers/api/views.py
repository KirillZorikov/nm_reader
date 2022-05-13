import asyncio

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from django.http import Http404

from parsers.models import Parser, Page
from parsers.api.serializers import InitPagesSerializer
from utils.browser import get_browser, create_pages
from utils.async_ import run_async


@api_view(('POST',))
@permission_classes((AllowAny,))
def init_pages(request):
    serializer = InitPagesSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    validated_data = serializer.validated_data

    if not validated_data.get('inited'):
        browser = get_browser(
            validated_data['type'], validated_data['service_slug']
        )
        pages_index = create_pages(browser, validated_data['service_slug'])
    else:
        pages_index = list(Page.objects.annotate_parser_slug().filter(
            parser_slug=validated_data['service_slug']
        ).values_list('index', flat=True))

    return Response(pages_index, status=status.HTTP_200_OK)
