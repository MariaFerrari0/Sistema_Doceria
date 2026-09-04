from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ProdutoForm
from .models import Produto


@login_required(login_url='administradora:login')
def listar(request):
    produtos = Produto.objects.all().order_by('-id')
    return render(request, 'produtos/pages/listar.html', {'produtos': produtos})


@login_required(login_url='administradora:login')
def detalhe(request, slug):
    produto = get_object_or_404(Produto, slug=slug)
    return render(request, 'produtos/pages/detalhe.html', {'produto': produto})


@login_required(login_url='administradora:login')
def criar(request):
    form = ProdutoForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Produto cadastrado com sucesso!')
        return redirect('produtos:listar')
    return render(request, 'produtos/pages/form.html', {'form': form, 'titulo': 'Cadastrar Produto'})


@login_required(login_url='administradora:login')
def editar(request, id):
    produto = get_object_or_404(Produto, id=id)
    form = ProdutoForm(request.POST or None, request.FILES or None, instance=produto)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Produto atualizado com sucesso!')
        return redirect('produtos:listar')
    return render(request, 'produtos/pages/form.html', {'form': form, 'titulo': 'Editar Produto'})


@login_required(login_url='administradora:login')
def alternar_status(request, id):
    produto = get_object_or_404(Produto, id=id)
    produto.ativo = not produto.ativo
    produto.save()
    status_str = 'ativado' if produto.ativo else 'desativado'
    messages.info(request, f'Produto {produto.nome} {status_str} com sucesso.')
    return redirect('produtos:listar')