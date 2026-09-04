from django.contrib import admin
from .models import PerfilAdministradora


@admin.register(PerfilAdministradora)
class PerfilAdministradoraAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'cargo', 'telefone')
    list_display_links = ('usuario',)