from django.contrib.auth.decorators import login_required
from django.utils import timezone
from products.forms import QuestionForm
from questions.models import Question
from django.shortcuts import render,redirect

@login_required(login_url='accounts:signin')
def question_modify(request, question_id):
    question = Question.objects.get(pk=question_id)
    if request.method=='POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():

            question.save()

            return redirect('products:detail', question.object_id)
    else :
        form = QuestionForm()
    return render(request, 'questions/question_create.html', {'form':form} )

@login_required(login_url='accounts:signin')
def question_delete(request, question_id):
    question = Question.objects.get(pk=question_id)
    question.delete()
    return redirect('products:detail', question.object_id)