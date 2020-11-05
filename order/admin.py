from django.contrib import admin

from order.models import ShoppingCart


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ['user', 'item', 'quantity', 'price', 'total']
    list_filter = ['user']


