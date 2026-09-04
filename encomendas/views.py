from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import EncomendaForm, StatusEncomendaForm
from .models import Encomenda


@login_required(login_url='administradora:login')
def listar(request):
    encomendas = Encomenda.objects.all().order_by('-data_criacao')
    return render(request, 'encomendas/pages/listar.html', {'encomendas': encomendas})


@login_required(login_url='administradora:login')
def detalhe(request, id):
    encomenda = get_object_or_404(Encomenda, id=id)
    form_status = StatusEncomendaForm(instance=encomenda)
    
    if request.method == 'POST':
        form_status = StatusEncomendaForm(request.POST, instance=encomenda)
        if form_status.is_valid():
            form_status.save()
            messages.success(request, f'Status da encomenda #{encomenda.id} atualizado!')
            return redirect('encomendas:detalhe', id=encomenda.id)

    context = {
        'encomenda': encomenda,
        'form_status': form_status,
    }
    return render(request, 'encomendas/pages/detalhe.html', context)


@login_required(login_url='administradora:login')
def criar(request):
    form = EncomendaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        encomenda = form.save()
        messages.success(request, f'Encomenda #{encomenda.id} registrada!')
        return redirect('encomendas:detalhe', id=encomenda.id)
    return render(request, 'encomendas/pages/form.html', {'form': form, 'titulo': 'Nova Encomenda'})


@login_required(login_url='administradora:login')
def cancelar(request, id):
    encomenda = get_object_or_404(Encomenda, id=id)
    encomenda.status = 'Cancelada'
    encomenda.save()
    messages.warning(request, f'Encomenda #{encomenda.id} foi cancelada.')
    return redirect('encomendas:listar')