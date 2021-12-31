from django import forms
from questions.models import Question
from cart.models import CartItem


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question  # 사용할 모델
        fields = ['body']
        labels = {
            'body': '내용',
        }

class CartForm(forms.ModelForm):
    class Meta:
        model = CartItem  # 사용할 모델
        fields = ['product_real', 'quantity']
        labels = {
            'product_real': '내용',
            'quantity' : '수량',
        }