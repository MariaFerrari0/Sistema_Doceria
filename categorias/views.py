from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import CategoriaForm
from .models import Categoria



@login_required(login_url='administradora:login')
def listar(request):
    categorias = Categoria.objects.all().order_by('-id')

    busca = request.GET.get('busca', '')
    status = request.GET.get('status', '')

    if busca:
        categorias = categorias.filter(nome__icontains=busca)

    if status == 'ativo':
        categorias = categorias.filter(ativo=True)
    elif status == 'inativo':
        categorias = categorias.filter(ativo=False)

    context = {
        'categorias': categorias,
        'busca': busca,
        'status_selecionado': status,
    }

    return render(request, 'categorias/pages/listar.html', context)



@login_required(login_url='administradora:login')
def criar(request):
    form = CategoriaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Categoria cadastrada com sucesso!')
        return redirect('categorias:listar')
    return render(request, 'categorias/pages/form.html', {'form': form, 'titulo': 'Cadastrar Categoria'})


@login_required(login_url='administradora:login')
def editar(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    form = CategoriaForm(request.POST or None, instance=categoria)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Categoria atualizada com sucesso!')
        return redirect('categorias:listar')
    return render(request, 'categorias/pages/form.html', {'form': form, 'titulo': 'Editar Categoria'})


@login_required(login_url='administradora:login')
def alternar_status(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    categoria.ativo = not categoria.ativo
    categoria.save()
    status_str = 'ativada' if categoria.ativo else 'desativada'
    messages.info(request, f'Categoria "{categoria.nome}" {status_str} com sucesso.')
    return redirect('categorias:listar')