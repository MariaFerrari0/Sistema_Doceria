from django.urls import path
from produtos import views

app_name = 'produtos'

urlpatterns = [
    path('', views.listar, name='listar'),
    path('<slug:slug>/', views.detalhe, name='detalhe'),
]