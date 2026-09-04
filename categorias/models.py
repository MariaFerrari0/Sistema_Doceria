from django.db import models


class Categoria(models.Model):
    nome = models.CharField(max_length=65)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.nome