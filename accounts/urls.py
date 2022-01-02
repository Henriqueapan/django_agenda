from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.login, name='index_login'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('dashboard/', views.dashboard, name='dashboard'),
]