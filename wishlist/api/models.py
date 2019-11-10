from django.db import models


class Client(models.Model):
    """
        Client Model
        Documentação dos atributos de Client
    """
    name = models.CharField('Nome', max_length=70)
    email = models.EmailField('E-mail', max_length=254, unique=True)

    class Meta:
        verbose_name = ('client')
        verbose_name_plural = ('clients')

    def __str__(self):
        return self.email


class Wishlist(models.Model):
    """
        Wishlist Model
        Documentação dos atributos de Wishlist
    """
    client = models.ForeignKey(
        Client,
        on_delete=models.deletion.CASCADE,
        related_name='wishlist'
    )
    product_id = models.CharField('Id do Produto', max_length=40)

    class Meta:
        # chave composta
        unique_together = (('client', 'product_id'))
