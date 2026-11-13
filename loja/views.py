
from django.shortcuts import render
from django.db.models import Sum, Q

from categorias.models import Categoria
from produtos.models import Produto


def home(request):
    categorias = Categoria.objects.filter(ativo=True)

    context = {
        'categorias': categorias
    }

    return render(request, 'home.html', context)


def catalogo(request):
    categorias = Categoria.objects.filter(ativo=True)
    produtos = Produto.objects.filter(ativo=True).select_related('categoria')

    categoria_id = request.GET.get('categoria')
    ordem = request.GET.get('ordem', 'vendidos')
    busca = request.GET.get('q', '').strip()

    # Busca pelo nome do produto
    if busca:
        produtos = produtos.filter(nome__icontains=busca)

    # Filtro por categoria
    if categoria_id and categoria_id.isdigit():
        produtos = produtos.filter(categoria_id=categoria_id)

    # Ordenação dos produtos
    if ordem == 'menor':
        produtos = produtos.order_by('preco', 'nome')

    elif ordem == 'maior':
        produtos = produtos.order_by('-preco', 'nome')

    else:
        produtos = produtos.annotate(
            total_vendido=Sum(
                'itemencomendaproduto__quantidade',
                filter=Q(
                    itemencomendaproduto__encomenda__status='Concluida'
                ),
                default=0
            )
        ).order_by('-total_vendido', 'nome')

    context = {
        'categorias': categorias,
        'produtos': produtos,
        'categoria_ativa': int(categoria_id)
        if categoria_id and categoria_id.isdigit()
        else None,
        'ordem_ativa': ordem,
        'busca': busca,
    }

    return render(request, 'catalogo.html', context)
