from django.urls import path

from parsers.api.views import init_pages


urlpatterns = [
    path('pages/init', init_pages),
]
