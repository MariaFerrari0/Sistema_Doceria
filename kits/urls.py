from django.urls import path
from kits import views

app_name = 'kits'

urlpatterns = [
    path('', views.listar, name='listar'),
]