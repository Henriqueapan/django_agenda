from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email as Vemail
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def login(request):
    if request.method != 'POST':
        return render(request, 'accounts/login.html')

    username = request.POST.get('username')
    senha = request.POST.get('password')

    user = auth.authenticate(request, username=username, password=senha)

    if not user:
        messages.error(request, 'Usuário ou senha inválidos.')
        return render(request, 'accounts/login.html')
    else:
        auth.login(request, user=user)
        messages.success(request, 'Você está logado')
        return redirect('dashboard')

def logout(request):
    auth.logout(request)
    return redirect('index')


def cadastro(request):
    # messages.success(request, 'Teste')
    # for message in messages.get_messages(request):
    #     message = ''

    if request.method != 'POST':
        return render(request, 'accounts/cadastro.html')

    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    email = request.POST.get('email') #if request.POST.get('email') != '' else None
    username = request.POST.get('username')# if request.POST.get('username') != '' else None
    senha = request.POST.get('password') # Inputs do tipo password enviam Nonetype caso não sejam preenchidos
    Rsenha = request.POST.get('Rpassword')

    if not nome or not sobrenome or not email or not username or not senha or not Rsenha:
        messages.error(request, 'Preencha todos os campos')

    try:
        if email:
            Vemail(email)
    except:
        messages.error(request, 'Email inválido')

    if username and len(username) < 6:
        messages.error(request, 'O nome de usuário precisa ter 6 caracteres ou mais')

    if senha and len(senha) < 6:
        messages.error(request, 'A senha precisa ter 6 caracteres ou mais')
    elif senha and Rsenha and senha!=Rsenha:
        messages.error(request, 'Os campos "Senha" e "Repetir senha" não coincidem')

    if User.objects.filter(username=username).exists():
        messages.error(request, 'Usuário já existente')

    if User.objects.filter(email=email).exists():
        messages.error(request, 'E-mail já cadastrado')

    message_list = list(messages.get_messages(request))

    print(request.POST)

    if not message_list and nome:
        messages.success(request, 'Usuário cadastrado com sucesso! Faça login para continuar.')
        user = User.objects.create_user(username=username, email=email, password=senha, first_name=nome,
                                        last_name=sobrenome)
        user.save()

        return redirect('login')
    else:
        return render(request, 'accounts/cadastro.html')

@login_required(redirect_field_name='login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')