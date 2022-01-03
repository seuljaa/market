from django import forms
from .models import CartItem


class CartForm(forms.ModelForm):
    class Meta:
        model = CartItem  # 사용할 모델
        fields = ['quantity']
        labels = {
            'quantity' : '수량',
        }