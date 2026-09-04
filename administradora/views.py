from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from produtos.models import Produto
from categorias.models import Categoria
from .forms import LoginForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('administradora:home')

    form = LoginForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Bem-vinda, {user.first_name or user.username}!')
            return redirect('administradora:home')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')

    return render(request, 'administradora/pages/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Sessão encerrada com sucesso.')
    return redirect('administradora:login')


@login_required(login_url='administradora:login')
def home(request):
    categorias = Categoria.objects.filter(ativo=True)
    categoria_id = request.GET.get('categoria')

    produtos = Produto.objects.filter(ativo=True)
    if categoria_id:
        produtos = produtos.filter(categoria_id=categoria_id)

    context = {
        'categorias': categorias,
        'produtos': produtos,
        'categoria_selecionada': categoria_id,
    }
    return render(request, 'administradora/pages/home.html', context)