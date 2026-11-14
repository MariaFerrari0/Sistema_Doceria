
from django import forms
from .models import Produto, Movimentacao


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


class MovimentacaoForm(forms.ModelForm):
    class Meta:
        model = Movimentacao
        fields = ['produto', 'tipo', 'quantidade', 'motivo']
        widgets = {
            'produto': forms.Select(attrs={'class': 'input-control'}),
            'tipo': forms.Select(attrs={'class': 'input-control'}),
            'quantidade': forms.NumberInput(attrs={
                'class': 'input-control',
                'min': '1'
            }),
            'motivo': forms.TextInput(attrs={
                'class': 'input-control',
                'placeholder': 'Informe o motivo da movimentação'
            }),
        }

    def clean_quantidade(self):
        quantidade = self.cleaned_data.get('quantidade')

        if quantidade is not None and quantidade < 1:
            raise forms.ValidationError(
                'A quantidade deve ser maior que zero.'
            )

        return quantidade
