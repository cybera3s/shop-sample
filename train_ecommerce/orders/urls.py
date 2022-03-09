
from django.urls import path
from .views import *

app_name = 'orders'

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/<int:product_id>', CartAddView.as_view(), name='cart_add'),
]