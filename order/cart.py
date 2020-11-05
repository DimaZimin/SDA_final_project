from decimal import Decimal
from django.conf import settings
from django.http import request
from store.models import Product
import logging

from store.models import ProductItem


class Cart(object):

    def __init__(self, request):

        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False, size=None):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)
        price = str(Product.objects.get(productitem__id=product_id).price)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': price, 'size': size}
        if override_quantity:
            print('\n\nTEST OVERRIDE QUANTITY')
            self.cart[product_id]['quantity'] = quantity
        else:
            print('\n\nTEST ELSE')
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = ProductItem.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()




