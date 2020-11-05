from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.conf import settings
from .cart import Cart
from .forms import CartAddProductForm
from .models import ShoppingCart, ShoppingCartForm
# Create your views here.
from store.models import Product
import logging

from store.models import ProductItem

from store.models import Size


@require_POST
def cart_add(request, product_id):
    url = request.META.get('HTTP_REFERER')
    cart = Cart(request)
    form = CartAddProductForm(request.POST)
    if url.endswith('cart/'):
        product = get_object_or_404(ProductItem, id=product_id)
        size = product.size
        quantity = int(request.POST['quantity'])
        if form.is_valid():
            cart.add(product=product,
                     quantity=quantity,
                     size=size,
                     override_quantity=True)
        return redirect('order:cart_detail')
    else:
        size = request.POST['size']
        product = get_object_or_404(ProductItem, product_id=product_id, size=Size.objects.get(name=size))
        quantity = int(request.POST['quantity'])
        if form.is_valid():
            cart.add(product=product,
                     quantity=quantity,
                     size=size)
        return HttpResponseRedirect(url)

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(ProductItem, id=product_id)
    cart.remove(product)
    return redirect('order:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'override': True})
    return render(request, 'order/detail.html', {'cart': cart})
