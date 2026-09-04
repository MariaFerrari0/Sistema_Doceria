from django.contrib import admin
from .models import Kit


@admin.register(Kit)
class KitAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'preco', 'ativo')
    list_display_links = ('nome',)
    list_editable = ('preco', 'ativo')
    search_fields = ('nome', 'descricao')
    list_filter = ('ativo',)
    filter_horizontal = ('produtos',)
    prepopulated_fields = {'slug': ('nome',)}