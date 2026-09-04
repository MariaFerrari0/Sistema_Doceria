from django.urls import path
from encomendas import views

app_name = 'encomendas'

urlpatterns = [
    path('', views.listar, name='listar'),
]