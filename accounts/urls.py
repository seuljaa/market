from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name='accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', auth_views.LoginView.as_view(template_name='accounts/signin.html'), name='signin'),
    path('signout/', auth_views.LogoutView.as_view(), name='logout'),
    path('find_id/', views.find_id, name='find_id'),
]
