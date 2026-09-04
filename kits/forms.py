from django import forms
from .models import Kit


class KitForm(forms.ModelForm):
    class Meta:
        model = Kit
        fields = ['nome', 'preco', 'descricao', 'imagem', 'produtos', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'input-control'}),
            'preco': forms.NumberInput(attrs={'class': 'input-control', 'step': '0.01', 'min': '0'}),
            'descricao': forms.Textarea(attrs={'class': 'input-control', 'rows': 4}),
            'imagem': forms.FileInput(attrs={'class': 'input-control'}),
            'produtos': forms.SelectMultiple(attrs={'class': 'input-control', 'style': 'height: 120px;'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'checkbox-control'}),
        }

    def clean_preco(self):
        preco = self.cleaned_data.get('preco')
        if preco is not None and preco < 0:
            raise forms.ValidationError('O preço do kit não pode ser negativo.')
        return preco