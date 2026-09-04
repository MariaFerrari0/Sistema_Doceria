from django.contrib import admin
from .models import Encomenda, ItemEncomendaKit, ItemEncomendaProduto


class ItemEncomendaProdutoInline(admin.TabularInline):
    model = ItemEncomendaProduto
    extra = 1


class ItemEncomendaKitInline(admin.TabularInline):
    model = ItemEncomendaKit
    extra = 1


@admin.register(Encomenda)
class EncomendaAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'status', 'valor_total', 'data_criacao', 'data_entrega')
    list_display_links = ('id', 'cliente')
    list_editable = ('status',)
    list_filter = ('status', 'data_criacao')
    search_fields = ('cliente__username', 'cliente__first_name')
    inlines = [ItemEncomendaProdutoInline, ItemEncomendaKitInline]