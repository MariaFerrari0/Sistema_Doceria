from django import forms
from .models import Encomenda


class EncomendaForm(forms.ModelForm):
    class Meta:
        model = Encomenda
        fields = ['cliente', 'data_entrega', 'status', 'valor_total']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'input-control'}),
            'data_entrega': forms.DateInput(attrs={'class': 'input-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'input-control'}),
            'valor_total': forms.NumberInput(attrs={'class': 'input-control', 'step': '0.01'}),
        }


class StatusEncomendaForm(forms.ModelForm):
    class Meta:
        model = Encomenda
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'input-control'}),
        }