from django import forms
from .models import Produto


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'categoria', 'preco', 'estoque', 'descricao', 'imagem', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'input-control'}),
            'categoria': forms.Select(attrs={'class': 'input-control'}),
            'preco': forms.NumberInput(attrs={'class': 'input-control', 'step': '0.01'}),
            'estoque': forms.NumberInput(attrs={'class': 'input-control'}),
            'descricao': forms.Textarea(attrs={'class': 'input-control', 'rows': 4}),
            'imagem': forms.FileInput(attrs={'class': 'input-control'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'checkbox-control'}),
        }