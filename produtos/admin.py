from django.contrib import admin
from .models import Produto


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'categoria', 'preco', 'estoque', 'ativo')
    list_display_links = ('nome',)
    list_editable = ('preco', 'estoque', 'ativo')
    search_fields = ('nome', 'descricao')
    list_filter = ('categoria', 'ativo')
    prepopulated_fields = {'slug': ('nome',)}