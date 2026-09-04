from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from categorias.models import Categoria
from produtos.models import Produto
from .forms import LoginForm, PerfilAdministradoraForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('administradora:home')

    form = LoginForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        lembrar_me = form.cleaned_data.get('lembrar_me', False)
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if not lembrar_me:
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(1209600)
                
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


# --- CRUD DO PERFIL DA ADMINISTRADORA ---

@login_required(login_url='administradora:login')
def perfil_ver(request):
    """Visualizar dados do próprio perfil."""
    return render(request, 'administradora/pages/perfil_ver.html', {'usuario': request.user})


@login_required(login_url='administradora:login')
def perfil_editar(request):
    """Editar dados e senha da conta da própria administradora."""
    form = PerfilAdministradoraForm(request.POST or None, instance=request.user)
    
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        # Mantém a sessão ativa caso a senha tenha sido alterada
        update_session_auth_hash(request, user)
        messages.success(request, 'Seu perfil foi atualizado com sucesso!')
        return redirect('administradora:perfil_ver')
        
    return render(request, 'administradora/pages/perfil_editar.html', {'form': form})


@login_required(login_url='administradora:login')
def perfil_excluir(request):
    """Excluir a própria conta da administradora."""
    user = request.user
    logout(request)
    user.delete()
    messages.warning(request, 'Sua conta de administradora foi excluída com sucesso.')
    return redirect('administradora:login')