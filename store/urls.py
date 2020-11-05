from django.urls import path
from . import views
from .models import Product
from .views import SubcategoryList, ProductDetail, GenderList

app_name = 'store'
urlpatterns = [
    path('<str:gender>/<str:subcategory>/<slug:slug>/', ProductDetail.as_view(), name='product-detail'),
    path('<str:gender>/<str:slug>/', SubcategoryList.as_view(), name='subcategory-product-list'),
    path('<str:gender>/', GenderList.as_view(), name='gender-category-list'),
    path('', views.IndexView.as_view(), name='home')
]
