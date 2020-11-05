from django.contrib import admin
from .models import Category, Product, Brand, SubCategory, Color, Size, Images, ProductItem


# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name', )}


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'gender', 'slug']
    prepopulated_fields = {'slug': ('name', )}


class ProductImageInline(admin.TabularInline):
    model = Images
    extra = 5


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['slug',  'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['available']
    prepopulated_fields = {'slug': ('name', )}
    inlines = [ProductImageInline]


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['slug', 'name', 'description']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'color_tag']


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'category']

@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    list_display = ['product', 'title', 'image']

@admin.register(ProductItem)
class Item(admin.ModelAdmin):
    list_display = ['name', 'product', 'size', 'color', 'quantity', 'on_sale']
