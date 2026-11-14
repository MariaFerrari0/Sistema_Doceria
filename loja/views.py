
from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction
from django.db.models import Sum, Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST

from categorias.models import Categoria
from produtos.models import Produto
from .forms import CadastroClienteForm
from .models import PerfilCliente


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

    if busca:
        produtos = produtos.filter(nome__icontains=busca)

    if categoria_id and categoria_id.isdigit():
        produtos = produtos.filter(categoria_id=categoria_id)

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


def detalhe_produto(request, slug):
    produto = get_object_or_404(
        Produto.objects.select_related('categoria'),
        slug=slug,
        ativo=True
    )

    context = {
        'produto': produto
    }

    return render(request, 'produto_detalhe.html', context)


@require_POST
def adicionar_carrinho(request, produto_id):
    produto = get_object_or_404(
        Produto,
        id=produto_id,
        ativo=True
    )

    try:
        quantidade = int(request.POST.get('quantidade', 1))
    except (TypeError, ValueError):
        quantidade = 0

    if quantidade < 1:
        messages.error(request, 'Informe uma quantidade válida.')
        return redirect('loja:detalhe_produto', slug=produto.slug)

    carrinho = request.session.get('carrinho', {})
    produto_id_str = str(produto.id)
    quantidade_atual = carrinho.get(produto_id_str, 0)

    if quantidade_atual + quantidade > produto.estoque:
        messages.error(
            request,
            'A quantidade solicitada ultrapassa o estoque disponível.'
        )
        return redirect('loja:detalhe_produto', slug=produto.slug)

    carrinho[produto_id_str] = quantidade_atual + quantidade
    request.session['carrinho'] = carrinho

    messages.success(
        request,
        f'{produto.nome} foi adicionado ao carrinho!'
    )

    return redirect('loja:detalhe_produto', slug=produto.slug)


def carrinho(request):
    carrinho_sessao = request.session.get('carrinho', {})

    produtos = Produto.objects.filter(
        id__in=carrinho_sessao.keys(),
        ativo=True
    )

    itens = []
    total = 0

    for produto in produtos:
        quantidade = carrinho_sessao.get(str(produto.id), 0)
        subtotal = produto.preco * quantidade

        itens.append({
            'id': produto.id,
            'nome': produto.nome,
            'preco': produto.preco,
            'imagem': produto.imagem,
            'quantidade': quantidade,
            'subtotal': subtotal,
            'estoque': produto.estoque,
        })

        total += subtotal

    context = {
        'itens': itens,
        'total': total,
    }

    return render(request, 'carrinho.html', context)


@require_POST
def atualizar_carrinho(request, produto_id):
    carrinho_sessao = request.session.get('carrinho', {})
    produto_id_str = str(produto_id)

    if produto_id_str not in carrinho_sessao:
        messages.error(request, 'Produto não encontrado no carrinho.')
        return redirect('loja:carrinho')

    produto = get_object_or_404(
        Produto,
        id=produto_id,
        ativo=True
    )

    try:
        quantidade = int(request.POST.get('quantidade', 1))
    except (TypeError, ValueError):
        quantidade = 0

    if quantidade < 1:
        messages.error(request, 'Informe uma quantidade válida.')
        return redirect('loja:carrinho')

    if quantidade > produto.estoque:
        messages.error(
            request,
            'A quantidade solicitada ultrapassa o estoque disponível.'
        )
        return redirect('loja:carrinho')

    carrinho_sessao[produto_id_str] = quantidade
    request.session['carrinho'] = carrinho_sessao

    messages.success(request, 'Quantidade atualizada.')

    return redirect('loja:carrinho')


@require_POST
def remover_carrinho(request, produto_id):
    carrinho_sessao = request.session.get('carrinho', {})
    produto_id_str = str(produto_id)

    if produto_id_str in carrinho_sessao:
        del carrinho_sessao[produto_id_str]
        request.session['carrinho'] = carrinho_sessao
        messages.success(request, 'Produto removido do carrinho.')

    return redirect('loja:carrinho')


@require_POST
def limpar_carrinho(request):
    request.session['carrinho'] = {}
    messages.success(request, 'Carrinho esvaziado.')

    return redirect('loja:carrinho')


def cadastro_cliente(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'perfil_cliente'):
            return redirect('loja:carrinho')

        return redirect('loja:home')

    form = CadastroClienteForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        try:
            with transaction.atomic():
                usuario = form.save(commit=False)
                usuario.save()

                PerfilCliente.objects.create(
                    usuario=usuario,
                    telefone=form.cleaned_data['telefone']
                )

            login(request, usuario)

            messages.success(
                request,
                'Cadastro realizado com sucesso! Confira seu carrinho.'
            )

            return redirect('loja:carrinho')

        except Exception:
            messages.error(
                request,
                'Não foi possível concluir seu cadastro. Tente novamente.'
            )

    return render(
        request,
        'cadastro.html',
        {'form': form}
    )


def login_cliente(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'perfil_cliente'):
            return redirect('loja:carrinho')

        return redirect('loja:home')

    if request.method == 'POST':
        email = request.POST.get('username', '').strip().lower()
        senha = request.POST.get('password', '')

        usuario = authenticate(
            request,
            username=email,
            password=senha
        )

        if usuario is not None and hasattr(usuario, 'perfil_cliente'):
            login(request, usuario)

            if request.POST.get('lembrar'):
                request.session.set_expiry(1209600)
            else:
                request.session.set_expiry(0)

            messages.success(
                request,
                'Login realizado com sucesso!'
            )

            return redirect('loja:carrinho')

        messages.error(
            request,
            'E-mail ou senha incorretos.'
        )

    return render(request, 'login.html')


def logout_cliente(request):
    if request.user.is_authenticated and hasattr(
        request.user, 'perfil_cliente'
    ):
        logout(request)

    return redirect('loja:home')


def finalizar_pedido(request):
    if not request.user.is_authenticated:
        return redirect('loja:login')

    if not hasattr(request.user, 'perfil_cliente'):
        messages.error(
            request,
            'Somente clientes podem finalizar pedidos.'
        )
        return redirect('loja:home')

    carrinho = request.session.get('carrinho', {})

    if not carrinho:
        messages.warning(request, 'Seu carrinho está vazio.')
        return redirect('loja:carrinho')

    return redirect('loja:carrinho')


