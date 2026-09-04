from django.db import models
from django.utils.text import slugify
from produtos.models import Produto
from sistema_doceria.validators import validar_preco_positivo


class Kit(models.Model):
    nome = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    descricao = models.TextField()
    preco = models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        validators=[validar_preco_positivo]
    )
    ativo = models.BooleanField(default=True)
    imagem = models.ImageField(upload_to='kits/%Y/%m/', blank=True, null=True)
    produtos = models.ManyToManyField(Produto, related_name='kits')

    class Meta:
        verbose_name = 'Kit'
        verbose_name_plural = 'Kits'

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)