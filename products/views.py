from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect
from products.models import Product
from questions.models import Question
from django.core.paginator import Paginator
from .forms import QuestionForm
from django.db.models import Q
# Create your views here.

def main(request):
    return render(request, 'main.html')

def product_list(request):
    page = request.GET.get('page', '1')
    search_keyword = request.GET.get('search_keyword', '')

    products = Product.objects.order_by('-reg_date')
    if search_keyword:
        products = products.filter(
            Q(display_name__icontains=search_keyword)
        ).distinct()
    paginator = Paginator(products, 10)
    page_obj = paginator.get_page(page)

    context = {'products':page_obj, 'page':page, 'search_keyword':search_keyword}
    return render(request, 'products/products_list.html', context)

def product_detail(request, product_id):
    products = Product.objects.get(pk=product_id)
    product_reals = products.productreal_set.order_by('option_1_display_name', 'option_2_display_name')
    ct = ContentType.objects.get_for_model(products)
    page = request.GET.get('page','1')
    questions = Question.objects.filter(content_type=ct,object_id=product_id)
    paginator = Paginator(questions, 5)
    page_obj = paginator.get_page(page)
    return render(request, 'products/products_detail.html', {'product_reals':product_reals, 'products':products, 'questions':page_obj} )

@login_required(login_url='accounts:signin')
def question_create(request, product_id):
    product = Product.objects.get(pk=product_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user.id
            question.object_id = product_id
            question.content_type = ContentType.objects.get_for_model(product)
            question.save()
            return redirect('products:detail', product_id=product.id)
    else :
        form = QuestionForm()
    return render(request, 'questions/question_create.html', {'form':form} )