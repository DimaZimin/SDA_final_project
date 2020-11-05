from django.contrib.auth.models import User

from django.db import models

from django.forms import ModelForm

from store.models import Product, ProductItem

from store.models import Size


class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    item = models.ForeignKey(ProductItem, on_delete=models.SET_NULL, blank=True, null=True)
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.item.name


    @property
    def price(self):
        return self.item.product.price

    @property
    def total(self):
        return self.quantity * self.item.product.price


class ShoppingCartForm(ModelForm):
    class Meta:
        model = ShoppingCart
        fields = ['quantity', 'size', 'item']



