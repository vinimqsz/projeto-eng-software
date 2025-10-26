from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('semestre/criar/', views.criar_semestre, name='criar_semestre'),
]