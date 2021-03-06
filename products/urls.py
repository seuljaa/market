
from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('list/', views.product_list, name='list'),
    path('list/<int:product_id>/', views.product_detail, name='detail'),
    path('list/<int:product_id>/question_create/',views.question_create,name='question_create'),
]