from django.urls import path
from .views import product_list, product_detail, add_product
from . import views

app_name = 'products'

urlpatterns = [
    path('', product_list, name='product_list'),
    path('product/<int:pk>/', product_detail, name='product_detail'),
    path('add-product/', views.add_product, name='add_product'),
    path('', views.product_list, name='product_list'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
]