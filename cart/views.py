from django.shortcuts import render, redirect
from .forms import CartForm

# Create your views here.


def cart_add(request):
    form = CartForm(request.POST)
    if form.is_valid():
        cart=form.save(commit=False)
        cart.user_id=request.user.id
        cart.product_real_id = 53
        cart.save()
        return redirect('products:detail', product_id=9)
