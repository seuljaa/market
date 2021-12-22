from django.shortcuts import render
from products.models import Product, ProductReal
# Create your views here.


def product_list(request):
    products = Product.objects.order_by('-reg_date')
    context = {'products':products}
    return render(request, 'products/products_list.html', context)

def product_detail(request, product_id):
    products = Product.objects.get(pk=product_id)
    context = {'products':products}
    return render(request, 'products/products_detail.html', context)