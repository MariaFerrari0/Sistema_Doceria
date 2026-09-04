from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import KitForm
from .models import Kit


@login_required(login_url='administradora:login')
def listar(request):
    kits = Kit.objects.all().order_by('-id')
    return render(request, 'kits/pages/listar.html', {'kits': kits})


@login_required(login_url='administradora:login')
def detalhe(request, slug):
    kit = get_object_or_404(Kit, slug=slug)
    return render(request, 'kits/pages/detalhe.html', {'kit': kit})


@login_required(login_url='administradora:login')
def criar(request):
    form = KitForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Kit de festa cadastrado com sucesso!')
        return redirect('kits:listar')
    return render(request, 'kits/pages/form.html', {'form': form, 'titulo': 'Cadastrar Kit'})


@login_required(login_url='administradora:login')
def editar(request, id):
    kit = get_object_or_404(Kit, id=id)
    form = KitForm(request.POST or None, request.FILES or None, instance=kit)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Kit atualizado com sucesso!')
        return redirect('kits:listar')
    return render(request, 'kits/pages/form.html', {'form': form, 'titulo': 'Editar Kit'})


@login_required(login_url='administradora:login')
def alternar_status(request, id):
    kit = get_object_or_404(Kit, id=id)
    kit.ativo = not kit.ativo
    kit.save()
    status_str = 'ativado' if kit.ativo else 'desativado'
    messages.info(request, f'Kit "{kit.nome}" {status_str} com sucesso.')
    return redirect('kits:listar')