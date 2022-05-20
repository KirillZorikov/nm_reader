from django.urls import path

from novels.api.views import (
    NovelServiceAPIView,
    ResourceListAPIView,
    ResourceAPIView,
    ServiceMainPageAPIView,
    ResourceFromUrlAPIView,
    SiteLanguageAPIView,
    ExtResourceFromUrlAPIView,
)

app_name = 'novels'
urlpatterns = [
    path(
        '',
        NovelServiceAPIView.as_view()
    ),
    path(
        'langs',
        SiteLanguageAPIView.as_view()
    ),
    path(
        'from-url',
        ExtResourceFromUrlAPIView.as_view(),
        name='ext_execute_from_url'
    ),
    path(
        '<lang_code>/<service>',
        ServiceMainPageAPIView.as_view()
    ),
    path(
        '<lang_code>/<service>/from-url',
        ResourceFromUrlAPIView.as_view(),
        name='execute_from_url'
    ),
    path(
        '<lang_code>/<service>/<resource_name>',
        ResourceAPIView.as_view()
    ),
]
