from django.urls import path

from parsers.api.views import (
    init_pages,
    set_service_pages_limit,
    set_service_timeout,
)


urlpatterns = [
    path('pages/init', init_pages),
    path('set_max_pages', set_service_pages_limit),
    path('set_timeout', set_service_timeout),
]
