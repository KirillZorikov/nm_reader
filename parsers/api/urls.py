from django.urls import path

from parsers.api.views import (
    TranslateParserListAPIView,
    TranslateParserRetrieveAPIView,
    captcha_solve,
    TranslateAPIView,
    pages_status,
)

urlpatterns = [
    path(
        'translate/list', 
        TranslateParserListAPIView.as_view(),
        name='translate_list'
    ),
    path(
        'translate/<slug:service>/languages', 
        TranslateParserRetrieveAPIView.as_view(),
        name='translate_detail'
    ),
    path(
        'translate/<slug:service>', 
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
