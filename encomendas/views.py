
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    EncomendaForm,
    StatusEncomendaForm,
    ItemEncomendaProdutoFormSet,
    ItemEncomendaKitFormSet,
)
from .models import Encomenda, ItemEncomendaProduto, ItemEncomendaKit


def calcular_total(produtos_formset, kits_formset):
    total = Decimal('0.00')

    for item in produtos_formset.cleaned_data:
        if item and not item.get('DELETE', False):
            produto = item.get('produto')
            quantidade = item.get('quantidade')

            if produto and quantidade:
                total += produto.preco * quantidade

    for item in kits_formset.cleaned_data:
        if item and not item.get('DELETE', False):
            kit = item.get('kit')
            quantidade = item.get('quantidade')

            if kit and quantidade:
                total += kit.preco * quantidade

    return total


@login_required(login_url='administradora:login')
def listar(request):
    encomendas = Encomenda.objects.all().order_by('-data_criacao')

    return render(
        request,
        'encomendas/pages/listar.html',
        {'encomendas': encomendas}
    )


@login_required(login_url='administradora:login')
def detalhe(request, id):
    encomenda = get_object_or_404(Encomenda, id=id)
    form_status = StatusEncomendaForm(instance=encomenda)

    if request.method == 'POST':
        form_status = StatusEncomendaForm(
            request.POST,
            instance=encomenda
        )

        if form_status.is_valid():
            form_status.save()

            messages.success(
                request,
                f'Status da encomenda #{encomenda.id} atualizado!'
            )

            return redirect('encomendas:detalhe', id=encomenda.id)

    context = {
        'encomenda': encomenda,
        'form_status': form_status,
    }

    return render(
        request,
        'encomendas/pages/detalhe.html',
        context
    )


@login_required(login_url='administradora:login')
def criar(request):
    form = EncomendaForm(request.POST or None)

    produtos_formset = ItemEncomendaProdutoFormSet(
        request.POST or None,
        instance=Encomenda()
    )

    kits_formset = ItemEncomendaKitFormSet(
        request.POST or None,
        instance=Encomenda()
    )

    if request.method == 'POST':
        if (
            form.is_valid()
            and produtos_formset.is_valid()
            and kits_formset.is_valid()
        ):
            total = calcular_total(
                produtos_formset,
                kits_formset
            )

            if total <= 0:
                messages.error(
                    request,
                    'Adicione pelo menos um produto ou kit à encomenda.'
                )
            else:
                with transaction.atomic():
                    encomenda = form.save(commit=False)
                    encomenda.valor_total = total
                    encomenda.save()

                    produtos_formset.instance = encomenda
                    kits_formset.instance = encomenda

                    produtos_formset.save()
                    kits_formset.save()

                messages.success(
                    request,
                    f'Encomenda #{encomenda.id} registrada com sucesso!'
                )

                return redirect(
                    'encomendas:detalhe',
                    id=encomenda.id
                )

    context = {
        'form': form,
        'produtos_formset': produtos_formset,
        'kits_formset': kits_formset,
        'titulo': 'Nova Encomenda',
    }

    return render(
        request,
        'encomendas/pages/form.html',
        context
    )


@login_required(login_url='administradora:login')
def editar(request, id):
    encomenda = get_object_or_404(Encomenda, id=id)

    form = EncomendaForm(
        request.POST or None,
        instance=encomenda
    )

    produtos_formset = ItemEncomendaProdutoFormSet(
        request.POST or None,
        instance=encomenda
    )

    kits_formset = ItemEncomendaKitFormSet(
        request.POST or None,
        instance=encomenda
    )

    if request.method == 'POST':
        if (
            form.is_valid()
            and produtos_formset.is_valid()
            and kits_formset.is_valid()
        ):
            total = calcular_total(
                produtos_formset,
                kits_formset
            )

            if total <= 0:
                messages.error(
                    request,
                    'A encomenda precisa ter pelo menos um produto ou kit.'
                )
            else:
                with transaction.atomic():
                    encomenda = form.save(commit=False)
                    encomenda.valor_total = total
                    encomenda.save()

                    produtos_formset.instance = encomenda
                    kits_formset.instance = encomenda

                    produtos_formset.save()
                    kits_formset.save()

                messages.success(
                    request,
                    f'Encomenda #{encomenda.id} atualizada com sucesso!'
                )

                return redirect(
                    'encomendas:detalhe',
                    id=encomenda.id
                )

    context = {
        'form': form,
        'produtos_formset': produtos_formset,
        'kits_formset': kits_formset,
        'titulo': f'Editar Encomenda #{encomenda.id}',
    }

    return render(
        request,
        'encomendas/pages/form.html',
        context
    )


@login_required(login_url='administradora:login')
def cancelar(request, id):
    encomenda = get_object_or_404(Encomenda, id=id)
    encomenda.status = 'Cancelada'
    encomenda.save()

    messages.warning(
        request,
        f'Encomenda #{encomenda.id} foi cancelada.'
    )

    return redirect('encomendas:listar')


@login_required(login_url='administradora:login')
def relatorios(request):
    encomendas = Encomenda.objects.all()

    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')

    if data_inicio:
        encomendas = encomendas.filter(
            data_criacao__date__gte=data_inicio
        )

    if data_fim:
        encomendas = encomendas.filter(
            data_criacao__date__lte=data_fim
        )

    totais_status = encomendas.values('status').annotate(
        quantidade=Count('id')
    ).order_by('status')

    total_encomendas = encomendas.count()

    faturamento = encomendas.filter(
        status='Concluida'
    ).aggregate(
        total=Sum('valor_total')
    )['total'] or Decimal('0.00')

    encomendas_concluidas = encomendas.filter(
        status='Concluida'
    )

    produtos_mais_vendidos = ItemEncomendaProduto.objects.filter(
        encomenda__in=encomendas_concluidas
    ).values(
        'produto__nome'
    ).annotate(
        quantidade_vendida=Sum('quantidade')
    ).order_by('-quantidade_vendida')[:10]

    kits_mais_vendidos = ItemEncomendaKit.objects.filter(
        encomenda__in=encomendas_concluidas
    ).values(
        'kit__nome'
    ).annotate(
        quantidade_vendida=Sum('quantidade')
    ).order_by('-quantidade_vendida')[:10]

    vendas_mensais = encomendas_concluidas.annotate(
        mes=TruncMonth('data_criacao')
    ).values(
        'mes'
    ).annotate(
        quantidade=Count('id'),
        faturamento=Sum('valor_total')
    ).order_by('mes')

    context = {
        'total_encomendas': total_encomendas,
        'totais_status': totais_status,
        'faturamento': faturamento,
        'produtos_mais_vendidos': produtos_mais_vendidos,
        'kits_mais_vendidos': kits_mais_vendidos,
        'vendas_mensais': vendas_mensais,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
    }

    return render(
        request,
        'encomendas/pages/relatorios.html',
        context
    )
