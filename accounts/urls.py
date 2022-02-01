from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.login, name='index_login'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('recuperacao/', views.recuperar_senha, name='recuperacao'),
    path('recuperacao_troca/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/troca-senha.html"), name='troca'),
    path('recuperacao_concluida', auth_views.PasswordResetCompleteView.as_view(template_name="accounts/recuperar-concluido.html"), name='password_reset_complete'),
]