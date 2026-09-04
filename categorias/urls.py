from django.urls import path
from categorias import views

app_name = 'categorias'

urlpatterns = [
    path('', views.listar, name='listar'),
    path('criar/', views.criar, name='criar'),
    path('editar/<int:id>/', views.editar, name='editar'),
    path('status/<int:id>/', views.alternar_status, name='status'),
]