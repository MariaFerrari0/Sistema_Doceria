from django.urls import path
from produtos import views

app_name = 'produtos'

urlpatterns = [
    path('', views.listar, name='listar'),
    path('criar/', views.criar, name='criar'),
    path('detalhe/<slug:slug>/', views.detalhe, name='detalhe'),
    path('editar/<int:id>/', views.editar, name='editar'),
    path('status/<int:id>/', views.alternar_status, name='status'),
    path('movimentacao/',views.movimentar_estoque, name='movimentar_estoque'),
    path('historico-movimentacoes/',views.historico_movimentacoes,name='historico_movimentacoes'),
]