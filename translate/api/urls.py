from django.urls import path

from translate.api.views import (
    TranslateParserListAPIView,
    TranslateParserRetrieveAPIView,
    captcha_solve,
    TranslateAPIView,
    pages_status,
)

urlpatterns = [
    path(
        'list', 
        TranslateParserListAPIView.as_view(),
        name='translate_list'
    ),
    path(
        '<slug:service>/languages', 
        TranslateParserRetrieveAPIView.as_view(),
        name='translate_detail'
    ),
    path(
        '<slug:service>', 
        TranslateAPIView.as_view(),
        name='translate'
    ),
    path(
        'captcha-solve',
        captcha_solve,
        name='captcha_solve'
    ),
    path(
        'pages/status',
        pages_status,
        name='pages_status'
    ),
]
