from django.contrib.auth.models import User
from django.db import models


class PerfilAdministradora(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_admin')
    cargo = models.CharField(max_length=50, default='Administradora')
    telefone = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name = 'Perfil da Administradora'
        verbose_name_plural = 'Perfis das Administradoras'

    def __str__(self):
        return f'{self.usuario.get_full_name() or self.usuario.username} ({self.cargo})'