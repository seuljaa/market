from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect
from products.models import Product
from questions.models import Question
from django.utils import timezone
from .forms import QuestionForm
# Create your views here.


def product_list(request):
    products = Product.objects.order_by('-reg_date')
    context = {'products':products}
    return render(request, 'products/products_list.html', context)

def product_detail(request, product_id):
    products = Product.objects.get(pk=product_id)
    product_reals = products.productreal_set.order_by('option_1_display_name', 'option_2_display_name')
    ct = ContentType.objects.get_for_model(products)
    questions = Question.objects.filter(content_type=ct,object_id=product_id)
    return render(request, 'products/products_detail.html', {'product_reals':product_reals, 'products':products, 'questions':questions} )

def question_create(request, product_id):
    product = Product.objects.get(pk=product_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user_id = 1
            question.object_id = product_id
            question.content_type = ContentType.objects.get_for_model(product)
            question.save()
            return redirect('products:detail', product_id=product.id)
    else :
        form = QuestionForm()
    return render(request, 'products/question_create.html', {'form':form} )