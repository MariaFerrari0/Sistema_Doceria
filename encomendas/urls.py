from django.urls import path
from encomendas import views

app_name = 'encomendas'

urlpatterns = [
    path('', views.listar, name='listar'),
    path('criar/', views.criar, name='criar'),
    path('detalhe/<int:id>/', views.detalhe, name='detalhe'),
    path('cancelar/<int:id>/', views.cancelar, name='cancelar'),
]