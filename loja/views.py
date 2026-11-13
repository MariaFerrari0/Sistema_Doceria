from django.shortcuts import render
from categorias.models import Categoria


def home(request):
    categorias = Categoria.objects.filter(ativo=True)

    context = {
        'categorias': categorias,
    }

    return render(
        request,
        'home.html',
        context
    )
