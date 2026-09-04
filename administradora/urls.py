from django.urls import path
from administradora import views

app_name = 'administradora'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Rotas do CRUD do Perfil da Administradora
    path('perfil/', views.perfil_ver, name='perfil_ver'),
    path('perfil/editar/', views.perfil_editar, name='perfil_editar'),
    path('perfil/excluir/', views.perfil_excluir, name='perfil_excluir'),
]