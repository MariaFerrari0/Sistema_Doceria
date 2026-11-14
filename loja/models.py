
from django.contrib.auth.models import User
from django.db import models


class PerfilCliente(models.Model):
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='perfil_cliente'
    )
    telefone = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Perfil do Cliente'
        verbose_name_plural = 'Perfis dos Clientes'

    def __str__(self):
        return self.usuario.get_full_name() or self.usuario.username
