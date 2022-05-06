from django.urls import path

from main.views import index_view

app_name = 'todos'
urlpatterns = [
    path('', index_view, name='index'),
]