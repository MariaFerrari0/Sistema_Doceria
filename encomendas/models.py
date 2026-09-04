from django.contrib.auth.models import User
from django.db import models
from kits.models import Kit
from produtos.models import Produto


class Encomenda(models.Model):
    STATUS_CHOICES = (
        ('Pendente', 'Pendente'),
        ('Em Producao', 'Em Produção'),
        ('Pronto', 'Pronto para Entrega/Retirada'),
        ('Concluida', 'Concluída'),
        ('Cancelada', 'Cancelada'),
    )

    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='encomendas')
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_entrega = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Pendente')
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
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