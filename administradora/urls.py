from django.urls import path
from administradora import views

app_name = 'administradora'

urlpatterns = [
    path('', views.home, name='home'),
]