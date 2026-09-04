from django.contrib.auth.models import User
from django.db import models
from kits.models import Kit
from produtos.models import Produto
from sistema_doceria.validators import validar_data_futura, validar_preco_positivo


class Encomenda(models.Model):
    STATUS_CHOICES = (
        ('Pendente', 'Pendente'),
        ('Em Producao', 'Em Produção'),
        ('Pronto', 'Pronto para Entrega/Retirada'),
        ('Concluida', 'Concluída'),
        ('Cancelada', 'Cancelada'),
    )

    # Torna os campos estritamente obrigatórios no banco
    cliente = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='encomendas', 
        null=False, 
        blank=False
    )
    data_criacao = models.DateTimeField(auto_now_add=True)

    data_entrega = models.DateField(
        null=False,
        blank=False,
        validators=[validar_data_futura]
    )
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Pendente')
    valor_total = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=False, 
        blank=False, 
        validators=[validar_preco_positivo]
    )
    produtos = models.ManyToManyField(Produto, through='ItemEncomendaProduto', blank=True)
    kits = models.ManyToManyField(Kit, through='ItemEncomendaKit', blank=True)

    class Meta:
        verbose_name = 'Encomenda'
        verbose_name_plural = 'Encomendas'

    def __str__(self):
        return f'Encomenda #{self.id} - {self.cliente.username}'


class ItemEncomendaProduto(models.Model):
    encomenda = models.ForeignKey(Encomenda, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)


class ItemEncomendaKit(models.Model):
    encomenda = models.ForeignKey(Encomenda, on_delete=models.CASCADE)
    kit = models.ForeignKey(Kit, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)