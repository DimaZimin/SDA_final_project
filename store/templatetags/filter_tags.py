from django import template
from store.models import SubCategory

from store.models import ProductItem

from store.models import Images

from store.models import Brand

from store.models import Product

from store.models import Color

register = template.Library()


@register.simple_tag()
def subcategory_tag(category_id, gender):
    subcategories_uni = SubCategory.objects.filter(parent_category_id=category_id, gender='unisex')
    subcategories = SubCategory.objects.filter(parent_category_id=category_id, gender=gender)
    return [*subcategories_uni, *subcategories]


@register.simple_tag()
def get_images_tag(product_id):
    images = Images.objects.filter(product_id=product_id)
    return images

@register.simple_tag()
def product_items_tag(product_id):
    items = ProductItem.objects.filter(product_id=product_id)
    return items

@register.simple_tag()
def brands_tag():
    brands = Brand.objects.all()
    return brands

@register.simple_tag()
def brands_amount_tag(brand_id):
    amount = Product.objects.filter(brand_id=brand_id).count()
    return amount

@register.simple_tag()
def color_amount_tag(color_id):
    amount = Color.objects.filter(id=color_id).count()
    return amount

@register.simple_tag()
def product_amount_by_gender_tag(gender):
    product_amount_by_gender = Product.objects.filter(gender=gender).count()
    return product_amount_by_gender


@register.simple_tag()
def colors_tag():
    return Color.objects.all()