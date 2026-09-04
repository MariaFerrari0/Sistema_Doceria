from django import forms
from .models import Categoria


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'input-control', 'placeholder': 'Nome da categoria'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'checkbox-control'}),
        }