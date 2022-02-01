from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email as Vemail
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from .models import FormContato


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


def recuperar_senha(request):

    if request.method != 'POST':
        return render(request, 'accounts/recuperar-conta.html')

    else:
        password_reset_email = request.POST.get('email')
        usuario = User.objects.filter(email=password_reset_email)

        if usuario.exists():
            subject = "Solicitação de troca de senha"
            email_template_name = "accounts/password_reset_email.txt"

            for user in usuario:
                mail_context = {
                    "email":user.email,
                    "domain":"127.0.0.1:8000",
                    "site_name":'Agenda',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                    "protocol": "http",
                }

                mail = render_to_string(email_template_name, mail_context)

                try:
                    send_mail(subject, mail, "henriqueandradepp@gmail.com", [user.email], fail_silently=False)
                except BadHeaderError:
                    messages.error(request, "Cabeçalho inválido encontrado! Tente novamente.")
                    return render(request, 'recuperacao', {"email":password_reset_email})

                messages.success(request, 'E-mail enviado! Verifique sua caixa de entrada.')
                return redirect('index')

@login_required(redirect_field_name='login')

def dashboard(request):
    if request.method != 'POST':
        form = FormContato()
        return render(request, 'accounts/dashboard.html', {'form': form})

    form = FormContato(request.POST, request.FILES)
    descricao = request.POST.get('descricao')

    if not form.is_valid():
        messages.error(request, 'Erro. Verifique os dados inseridos.')
        form = FormContato(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form})

    if len(descricao) < 5:
        messages.error(request, "A descrição precisa ter mais que 5 caracteres.")
        form = FormContato(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form})

    form.save()
    messages.success(request, f"Contato {request.POST.get('nome')} {request.POST.get('sobrenome')} criado com sucesso!")
    return redirect('dashboard')