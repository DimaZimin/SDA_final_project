from urllib import request

from rest_framework import viewsets
from rest_framework import permissions
from django.http import Http404
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import View, TemplateView, ListView
from django.views.generic.detail import DetailView
from .models import Product, Category, SubCategory, GENDER_CHOICES, Brand, ProductItem, Size, Color
from .context_processors import static_categories
from order.models import ShoppingCartForm

from order.forms import CartAddProductForm

from store.serializers import ProductSerializer


class IndexView(TemplateView):
    template_name = 'store/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class GenderList(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'store/gender_category_list.html'

    def get_queryset(self):
        gender = self.kwargs.get('gender')
        queryset = Product.objects.filter(gender=gender)
        if queryset:
            return queryset
        else:
            raise Http404


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_gender'] = self.kwargs.get('gender')
        context['genders'] = [gender[0] for gender in GENDER_CHOICES]
        context['brands'] = Brand.objects.all()
        context['colors'] = Color.objects.all()
        return context


class SubcategoryList(ListView):
    model = SubCategory
    context_object_name = 'products'
    template_name = 'store/subcategory_detail.html'

    def get_queryset(self):
        gender = self.kwargs.get('gender')
        subcategory = get_object_or_404(SubCategory, slug=self.kwargs.get('slug'))
        queryset = Product.objects.filter(subcategory__name=subcategory, gender=gender)
        if queryset:
            return queryset
        else:
            raise Http404

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_gender'] = self.kwargs.get('gender')
        context['genders'] = [gender[0] for gender in GENDER_CHOICES]
        context['subcategory'] = get_object_or_404(SubCategory, slug=self.kwargs.get('slug'))
        context['brands'] = Brand.objects.all()
        context['colors'] = Color.objects.all()
        return context


class ProductDetail(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'store/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = self.object
        context['genders'] = [gender[0] for gender in GENDER_CHOICES]
        context['current_gender'] = self.kwargs.get('gender')
        context['brands'] = Brand.objects.all()
        context['items'] = ProductItem.objects.filter(product_id=self.object.id)
        context['cart_product_form'] = CartAddProductForm()
        try:
            context['item_size'] = str(self.request.GET['size'])
            context['price'] = ProductItem.objects.get(product_id=self.object.id, size=Size.objects.get(name=context['item_size']))
        except MultiValueDictKeyError:
            pass
        return context

class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

