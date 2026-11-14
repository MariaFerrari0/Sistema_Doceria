
from django.urls import path
from . import views

app_name = 'loja'

urlpatterns = [
    path('', views.home, name='home'),
    path('catalogo/', views.catalogo, name='catalogo'),

    path(
        'produto/<slug:slug>/',
        views.detalhe_produto,
        name='detalhe_produto'
    ),

    path('carrinho/', views.carrinho, name='carrinho'),

    path(
        'carrinho/adicionar/<int:produto_id>/',
        views.adicionar_carrinho,
        name='adicionar_carrinho'
    ),

    path(
        'carrinho/atualizar/<int:produto_id>/',
        views.atualizar_carrinho,
        name='atualizar_carrinho'
    ),

    path(
        'carrinho/remover/<int:produto_id>/',
        views.remover_carrinho,
        name='remover_carrinho'
    ),

    path(
        'carrinho/limpar/',
        views.limpar_carrinho,
        name='limpar_carrinho'
    ),

    path(
        'finalizar-pedido/',
        views.finalizar_pedido,
        name='finalizar_pedido'
    ),

    path('cadastro/', views.cadastro_cliente, name='cadastro'),
    path('login/', views.login_cliente, name='login'),
    path('logout/', views.logout_cliente, name='logout'),

    path('meus-pedidos/', views.meus_pedidos, name='meus_pedidos'),
    path('meus-pedidos/<int:encomenda_id>/cancelar/',views.cancelar_meu_pedido,name='cancelar_meu_pedido'),
]
