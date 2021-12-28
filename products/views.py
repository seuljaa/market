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


def product_list(request):
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')
    products = Product.objects.order_by('-reg_date')
    if kw:
        product_list = products.filter(
            Q(subject__icontains=kw) |  # 제목검색
            Q(content__icontains=kw) |  # 내용검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이검색
        ).distinct()
    paginator = Paginator(products, 10)
    page_obj = paginator.get_page(page)
    context = {'products':page_obj, 'page':page, 'kw':kw}
    return render(request, 'products/products_list.html', context)

def product_detail(request, product_id):
    products = Product.objects.get(pk=product_id)
    product_reals = products.productreal_set.order_by('option_1_display_name', 'option_2_display_name')
    ct = ContentType.objects.get_for_model(products)
    page = request.GET.get('page','1')
    questions = Question.objects.filter(content_type=ct,object_id=product_id)
    paginator = Paginator(questions, 10)
    page_obj = paginator.get_page(page)
    return render(request, 'products/products_detail.html', {'product_reals':product_reals, 'products':products, 'questions':page_obj} )

@login_required(login_url='accounts:signin')
def question_create(request, product_id):
    product = Product.objects.get(pk=product_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user_id = request.user.id
            question.object_id = product_id
            question.content_type = ContentType.objects.get_for_model(product)
            question.save()
            messages.success(request, "질문이 등록되었습니다.")
            return redirect('products:detail', product_id=product.id)
    else :
        form = QuestionForm()
    return render(request, 'questions/question_create.html', {'form':form} )