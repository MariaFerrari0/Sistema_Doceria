from django.urls import path
from kits import views

app_name = 'kits'

urlpatterns = [
    path('', views.listar, name='listar'),
    path('criar/', views.criar, name='criar'),
    path('detalhe/<slug:slug>/', views.detalhe, name='detalhe'),
    path('editar/<int:id>/', views.editar, name='editar'),
    path('status/<int:id>/', views.alternar_status, name='status'),
]