from django import forms

from products.models import ProductReal
from .models import CartItem


class CartForm(forms.ModelForm):
    class Meta:
        model = CartItem  # 사용할 모델
        fields = ['quantity']