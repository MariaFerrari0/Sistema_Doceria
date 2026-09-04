from django import forms
from django.utils import timezone
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].required = True
        self.fields['data_entrega'].required = True
        self.fields['valor_total'].required = True

    def clean_data_entrega(self):
        data_entrega = self.cleaned_data.get('data_entrega')
        if data_entrega and data_entrega < timezone.now().date():
            raise forms.ValidationError('A data de entrega não pode ser anterior à data atual.')
        return data_entrega

    def clean_valor_total(self):
        valor = self.cleaned_data.get('valor_total')
        if valor is not None and valor < 0:
            raise forms.ValidationError('O valor total não pode ser negativo.')
        return valor


# Form dedicado apenas à alteração rápida do Status da Encomenda
class StatusEncomendaForm(forms.ModelForm):
    class Meta:
        model = Encomenda
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'input-control'}),
        }