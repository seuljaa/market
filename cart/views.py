from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from products.models import ProductReal
from .forms import CartForm
from .models import CartItem
from products.models import Product
from django.http import HttpResponse

# Create your views here.

@login_required(login_url='accounts:signin')
def cart_add(request, product_id):
    product_real_size = request.POST.get('size')
    product_real_color = request.POST.get('color')
    for value in ProductReal.objects.all():
        if value.product_id == product_id and value.option_1_name == product_real_size and value.option_2_name == product_real_color :
            index = value.id
            id = value.product_id
            form = CartForm(request.POST)
            if form.is_valid():
                cart=form.save(commit=False)
                cart.user_id=request.user.id
                cart.product_real_id = index
                cart.save()
                return redirect('products:detail', product_id=id)

@login_required(login_url='accounts:signin')
def cart_list(request):
    cartitem = CartItem.objects.filter(user=request.user)
    product_real = ProductReal.objects.all()
    product = Product.objects.all()
    return render(request, 'cart/cart_list.html', {'cartitem': cartitem,'product_real':product_real, 'product':product })