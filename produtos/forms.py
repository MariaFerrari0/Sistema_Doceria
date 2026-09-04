from django import forms
from .models import Produto


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'categoria', 'preco', 'estoque', 'descricao', 'imagem', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'input-control'}),
            'categoria': forms.Select(attrs={'class': 'input-control'}),
            'preco': forms.NumberInput(attrs={'class': 'input-control', 'step': '0.01', 'min': '0'}),
            'estoque': forms.NumberInput(attrs={'class': 'input-control', 'min': '0'}),
            'descricao': forms.Textarea(attrs={'class': 'input-control', 'rows': 4}),
            'imagem': forms.FileInput(attrs={'class': 'input-control'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'checkbox-control'}),
        }

    def clean_preco(self):
        preco = self.cleaned_data.get('preco')
        if preco is not None and preco < 0:
            raise forms.ValidationError('O preço do produto não pode ser negativo.')
        return preco

    def clean_estoque(self):
        estoque = self.cleaned_data.get('estoque')
        if estoque is not None and estoque < 0:
            raise forms.ValidationError('O estoque não pode ser negativo.')
        return estoque