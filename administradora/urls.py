from django.urls import path
from administradora.views import home

urlpatterns = [
    path('', home),
]