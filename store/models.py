import os

from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django_countries.fields import CountryField
from django.conf import settings
from django.urls import reverse
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)


GENDER_CHOICES = (
    ('unisex', 'Unisex'),
    ('male', 'Male'),
    ('female', 'Female')
)

LABEL_CHOISES= (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)


class Brand(models.Model):
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=250)
    slug = models.SlugField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=30)
    parent_category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                        null=True,
                                        blank=True, default=None, related_name='subcategory')
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10)
    description = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        ordering = ('name',)
        verbose_name = 'Sub category'
        verbose_name_plural = 'Sub categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:product_list_by_category', args=[self.gender, self.name])


class Size(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name

    def color_tag(self):
        if self.code is not None:
            return mark_safe(f'<p style="background-color:{self.code}>{self.name}</p>"')
        else:
            return ''


def get_upload_path(instance, filename):
    return os.path.join(
      "%s" % instance.subcategory, "%s" % instance.slug, filename)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=200, db_index=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.SlugField(max_length=200, db_index=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    image = models.ImageField(upload_to=get_upload_path, blank=True)
    description = models.TextField(blank=True)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:product-detail', args=[self.gender, self.subcategory, self.slug])

    def quantity(self):
        return ProductItem.objects.filter(product_id=self.id)


class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True)
    image = models.ImageField(blank=True, upload_to='images')

    def __str__(self):
        return self.title


class ProductItem(models.Model):
    name = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=1)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    image_id = models.ImageField(blank=True, null=True, default=0)
    on_sale = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.color} {self.name} size {self.size}'

    def image(self):
        img = Images.objects.get(image=self.image_id)
        if img.id:
            item_image = img.image.url
        else:
            item_image = ''
        return item_image

    def image_tag(self):
        img = Images.objects.get(id=self.image_id)
        if img.id:
            return mark_safe('<img src="{}" height="50"/>'.format(img.image.url))
        else:
            return ''


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    telephone = models.CharField(max_length=200)


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street_address = models.CharField(max_length=200)
    apartment_address = models.CharField(max_length=200)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=10)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user

    class Meta:
        verbose_name_plural = 'Addresses'


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    # def __str__(self):
    #     return str(self.id)


class OrderItem(models.Model):
    product = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    street_address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    country = CountryField(multiple=False)
    zipcode = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.street_address

