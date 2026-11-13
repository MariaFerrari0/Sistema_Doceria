
from django import forms
from django.utils import timezone
from django.forms import inlineformset_factory

from .models import (
    Encomenda,
    ItemEncomendaProduto,
    ItemEncomendaKit,
)


class EncomendaForm(forms.ModelForm):
    class Meta:
        model = Encomenda
        fields = ['cliente', 'data_entrega', 'status', 'valor_total']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'input-control'}),
            'data_entrega': forms.DateInput(
                attrs={'class': 'input-control', 'type': 'date'}
            ),
            'status': forms.Select(attrs={'class': 'input-control'}),
            'valor_total': forms.NumberInput(
                attrs={'class': 'input-control', 'step': '0.01'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].required = True
        self.fields['data_entrega'].required = True
        self.fields['valor_total'].required = False

    def clean_data_entrega(self):
        data_entrega = self.cleaned_data.get('data_entrega')

        if data_entrega and data_entrega < timezone.now().date():
            raise forms.ValidationError(
                'A data de entrega não pode ser anterior à data atual.'
            )

        return data_entrega

    def clean_valor_total(self):
        valor = self.cleaned_data.get('valor_total')

        if valor is not None and valor < 0:
            raise forms.ValidationError(
                'O valor total não pode ser negativo.'
            )

        return valor


class ItemEncomendaProdutoForm(forms.ModelForm):
    quantidade = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(
            attrs={'class': 'input-control', 'min': 1}
        )
    )

    class Meta:
        model = ItemEncomendaProduto
        fields = ['produto', 'quantidade']
        widgets = {
            'produto': forms.Select(
                attrs={'class': 'input-control'}
            ),
        }


class ItemEncomendaKitForm(forms.ModelForm):
    quantidade = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(
            attrs={'class': 'input-control', 'min': 1}
        )
    )

    class Meta:
        model = ItemEncomendaKit
        fields = ['kit', 'quantidade']
        widgets = {
            'kit': forms.Select(
                attrs={'class': 'input-control'}
            ),
        }


ItemEncomendaProdutoFormSet = inlineformset_factory(
    Encomenda,
    ItemEncomendaProduto,
    form=ItemEncomendaProdutoForm,
    extra=1,
    can_delete=True,
)


ItemEncomendaKitFormSet = inlineformset_factory(
    Encomenda,
    ItemEncomendaKit,
    form=ItemEncomendaKitForm,
    extra=1,
    max_num=1,
    validate_max=True,
    can_delete=False,
)


# Form dedicado apenas à alteração rápida do Status da Encomenda
class StatusEncomendaForm(forms.ModelForm):
    class Meta:
        model = Encomenda
        fields = ['status']
        widgets = {
            'status': forms.Select(
                attrs={'class': 'input-control'}
            ),
        }
