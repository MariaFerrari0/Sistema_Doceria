from django.urls import path
from categorias import views

app_name = 'categorias'

urlpatterns = [
    path('', views.listar, name='listar'),
]