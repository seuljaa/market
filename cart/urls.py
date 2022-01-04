from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('<int:product_id>/', views.cart_add, name='add'),
    path('list/', views.cart_list, name='cart_list'),
]