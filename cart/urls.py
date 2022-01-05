from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('<int:product_id>/', views.cart_add, name='add'),
    path('list/', views.cart_list, name='cart_list'),
    path('<int:product_real_id>/list/<int:item_id>/modify/', views.cart_modify, name='cart_modify')
]