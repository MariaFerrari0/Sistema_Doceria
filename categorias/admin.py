from django.contrib import admin
from .models import Categoria


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'ativo')
    list_display_links = ('nome',)
    list_editable = ('ativo',)
    search_fields = ('nome',)
    list_filter = ('ativo',)