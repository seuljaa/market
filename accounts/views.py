import os

from django.http import HttpResponse
import requests
from accounts import models
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, login
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
            first_name = form.cleaned_data['first_name']

            qs:QuerySet = User.objects.filter(email=email, first_name=first_name)

            if not qs.exists():
                messages.warning(request, "일치하는 회원이 존재하지 않습니다.")
            else:
                user: User = qs.first()
                messages.success(request, f"해당회원의 사용자ID는 {user.username} 입니다.")
                return redirect(reverse("accounts:signin") + '?username=' + user.username)
    else:
        form = FindUsernameForm()

    return render(request, 'accounts/find_id.html', {'form': form,})


def kakao_signin(request):
    client_id = os.environ.get("KAKAO_ID")
    REDIRECT_URI = "http://localhost:8000/accounts/signin/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={REDIRECT_URI}&response_type=code"
    )

def kakao_signin_callback(request):
        # (1)
        code = request.GET.get("code")
        client_id = os.environ.get("KAKAO_ID")
        REDIRECT_URI = "http://localhost:8000/accounts/signin/kakao/callback"
        # (2)
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={REDIRECT_URI}&code={code}"
        )
        # (3)
        token_json = token_request.json()

        # (4)
        access_token = token_json.get("access_token")
        # (5)
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()
        email = profile_json.get("kakao_account", None).get("email")
        nickname = profile_json.get("kakao_account", None).get("profile", None).get("nickname")
        # (7)
        try:
            user = models.User.objects.get(email=email)

        except models.User.DoesNotExist:
            user = models.User.objects.create(
                email=email,
                username=email,
                first_name=nickname,
                last_name=nickname,
            )
            user.set_unusable_password()
            user.save()

        login(request, user)
        return redirect('main')

