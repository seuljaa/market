from django.shortcuts import render, redirect
from products.models import ProductReal
from .forms import CartForm

# Create your views here.


def cart_add(request, product_id):
    product_real_size=request.GET.get('size')
    product_real_color=request.GET.get('color')
    for value in ProductReal.objects.all():
        if value.id==53:
            index = value.id
    form = CartForm(request.POST)
    if form.is_valid():
        cart=form.save(commit=False)
        cart.user_id=request.user.id
        cart.product_real_id = index
        cart.save()
        return redirect('products:detail', product_id=9)
