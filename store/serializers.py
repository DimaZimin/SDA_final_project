from .models import ProductItem, Product, Brand, Category, SubCategory
from rest_framework import serializers


class ProductSerializer(serializers.HyperlinkedRelatedField):
    url = serializers.HyperlinkedIdentityField(view_name="store:product-detail")

    class Meta:
        model = Product
        fields = ['id', 'category', 'subcategory', 'name', 'brand', 'price', 'gender', 'image', 'description',
                  'description', 'available', 'created', 'updated', 'url']


class ProductItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductItem
        fields = ['name', 'product', 'size', 'color', 'quantity', 'image_id', 'on_sale']


class BrandSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Brand
        fields = ['name', 'description']


class CategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Category
        fields = ['name', 'description']


class SubCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['name', 'parent_category', 'gender', 'description']


class SizeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'code', 'category']


