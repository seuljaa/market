from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.db.models import QuerySet
from django.urls import reverse


from accounts.forms import SignupForm, FindUsernameForm
from .models import User

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            signed_user = form.save()
            auth_login(request, signed_user)
            messages.success(request, "회원가입 환영합니다.")
            # signed_user.send_welcome_email()  # FIXME: Celery로 처리하는 것을 추천.
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {
        'form': form,
    })

def find_id(request):
    if request.method == 'POST':
        form = FindUsernameForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            last_name = form.cleaned_data['last_name']

            qs:QuerySet = User.objects.filter(email=email, last_name=last_name)

            if not qs.exists():
                messages.warning(request, "일치하는 회원이 존재하지 않습니다.")
            else:
                user: User = qs.first()
                messages.success(request, f"해당회원의 사용자ID는 {user.username} 입니다.")
                return redirect(reverse("accounts:signin") + '?username=' + user.username)
    else:
        form = FindUsernameForm()

    return render(request, 'accounts/find_id.html', {'form': form,})
