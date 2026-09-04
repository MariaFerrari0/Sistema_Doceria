from django import forms
from .models import Categoria


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'descricao', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'input-control'}),
            'descricao': forms.Textarea(attrs={'class': 'input-control', 'rows': 3}),
            'ativo': forms.CheckboxInput(attrs={'class': 'checkbox-control'}),
        }