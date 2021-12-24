from . import views
from django.urls import path


app_name = 'question'

urlpatterns = [
    path('<int:question_id>/question_modify/', views.question_modify, name='question_modify'),
    path('<int:question_id>/question_delete/', views.question_delete, name='question_delete'),
]