
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import F, Sum, Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProdutoForm, MovimentacaoForm
from .models import Produto, Movimentacao


@login_required(login_url='administradora:login')
def listar(request):
    produtos = Produto.objects.all().order_by('-id')

    busca = request.GET.get('busca', '')
    categoria_id = request.GET.get('categoria', '')
    status = request.GET.get('status', '')

    if busca:
        produtos = produtos.filter(nome__icontains=busca)

    if categoria_id:
        produtos = produtos.filter(categoria_id=categoria_id)

    if status == 'ativo':
        produtos = produtos.filter(ativo=True)
    elif status == 'inativo':
        produtos = produtos.filter(ativo=False)

    categorias = Produto._meta.get_field('categoria').related_model.objects.all().order_by('nome')

    context = {
        'produtos': produtos,
        'categorias': categorias,
        'busca': busca,
        'categoria_selecionada': categoria_id,
        'status_selecionado': status,
    }

    return render(
        request,
        'produtos/pages/listar.html',
        context
    )


@login_required(login_url='administradora:login')
def detalhe(request, slug):
    produto = get_object_or_404(Produto, slug=slug)
    return render(
        request,
        'produtos/pages/detalhe.html',
        {'produto': produto}
    )


@login_required(login_url='administradora:login')
def criar(request):
    form = ProdutoForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Produto cadastrado com sucesso!')
        return redirect('produtos:listar')

    return render(
        request,
        'produtos/pages/form.html',
        {'form': form, 'titulo': 'Cadastrar Produto'}
    )


@login_required(login_url='administradora:login')
def editar(request, id):
    produto = get_object_or_404(Produto, id=id)
    form = ProdutoForm(
        request.POST or None,
        request.FILES or None,
        instance=produto
    )

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Produto atualizado com sucesso!')
        return redirect('produtos:listar')

    return render(
        request,
        'produtos/pages/form.html',
        {'form': form, 'titulo': 'Editar Produto'}
    )


@login_required(login_url='administradora:login')
def alternar_status(request, id):
    produto = get_object_or_404(Produto, id=id)
    produto.ativo = not produto.ativo
    produto.save()

    status_str = 'ativado' if produto.ativo else 'desativado'

    messages.info(
        request,
        f'Produto {produto.nome} {status_str} com sucesso.'
    )

    return redirect('produtos:listar')


@login_required(login_url='administradora:login')
def movimentar_estoque(request):
    if request.method == 'POST':
        form = MovimentacaoForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                produto_id = form.cleaned_data['produto'].id

                produto = get_object_or_404(
                    Produto.objects.select_for_update(),
                    id=produto_id
                )

                quantidade = form.cleaned_data['quantidade']
                tipo = form.cleaned_data['tipo']

                if tipo == 'Saida' and quantidade > produto.estoque:
                    form.add_error(
                        'quantidade',
                        'Estoque insuficiente para realizar esta saída.'
                    )
                else:
                    if tipo == 'Entrada':
                        Produto.objects.filter(id=produto.id).update(
                            estoque=F('estoque') + quantidade
                        )
                    else:
                        Produto.objects.filter(id=produto.id).update(
                            estoque=F('estoque') - quantidade
                        )

                    movimentacao = form.save(commit=False)
                    movimentacao.responsavel = request.user
                    movimentacao.save()

                    messages.success(
                        request,
                        'Movimentação registrada e estoque atualizado!'
                    )

                    return redirect('produtos:listar')
    else:
        form = MovimentacaoForm()

    return render(
        request,
        'produtos/pages/movimentacao.html',
        {'form': form, 'titulo': 'Movimentação de Estoque'}
    )


@login_required(login_url='administradora:login')
def historico_movimentacoes(request):
    movimentacoes = Movimentacao.objects.select_related(
        'produto',
        'responsavel'
    ).order_by('-data_movimentacao')

    produto_id = request.GET.get('produto')
    tipo = request.GET.get('tipo')
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')

    if produto_id:
        movimentacoes = movimentacoes.filter(produto_id=produto_id)

    if tipo:
        movimentacoes = movimentacoes.filter(tipo=tipo)

    if data_inicio:
        movimentacoes = movimentacoes.filter(
            data_movimentacao__date__gte=data_inicio
        )

    if data_fim:
        movimentacoes = movimentacoes.filter(
            data_movimentacao__date__lte=data_fim
        )

    produtos = Produto.objects.all().order_by('nome')

    totais = movimentacoes.aggregate(
        total_entradas=Sum(
            'quantidade',
            filter=Q(tipo='Entrada')
        ),
        total_saidas=Sum(
            'quantidade',
            filter=Q(tipo='Saida')
        )
    )

    total_entradas = totais['total_entradas'] or 0
    total_saidas = totais['total_saidas'] or 0

    return render(
        request,
        'produtos/pages/historico_movimentacoes.html',
        {
            'movimentacoes': movimentacoes,
            'produtos': produtos,
            'produto_selecionado': produto_id,
            'tipo_selecionado': tipo,
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'total_entradas': total_entradas,
            'total_saidas': total_saidas,
            'titulo': 'Histórico de Movimentações'
        }
    )
