from django.core.exceptions import ValidationError
from django.utils import timezone


def validar_preco_positivo(valor):
    """Garante que preços e valores totais não sejam negativos."""
    if valor is not None and valor < 0:
        raise ValidationError('O valor não pode ser negativo.')


def validar_data_futura(data):
    """Garante que a data de entrega não seja anterior ao dia de hoje."""
    if data and data < timezone.now().date():
        raise ValidationError('A data de entrega não pode ser anterior à data atual.')