from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants

def login(request):
    status = request.GET.get('status', None)
    return render(request,'login.html', {'status': status})

def cadastro(request):
    status = request.GET.get('status', None)
    return render(request, 'cadastro.html', {'status': status})

def validar_login(request):
    pes_email = request.POST.get('email')
    pes_senha = request.POST.get('senha')
    
    Usuario = usuario.objects.filter(email=email, senha=senha)
    
    if not Usuario.exists():
        messages.add_message(request, constants.WARNING, 'Email ou senha inválidos')
        return redirect('/auth/login')
    else:
        request.session['logado'] = True
        return redirect('/plataforma/home')
    

def validar_cadastro(request):
    pes_nome = request.POST.get('nome')
    pes_sobrenome = request.POST.get('sobrenome')
    pes_email = request.POST.get('email')
    pes_senha = request.POST.get('senha')
    emp_nome = request.POST.get('emp_nome')
    emp_nova = request.POST.get('emp_nova')
    
    if len(pes_nome.strip()) == 0 or len(pes_email.strip()) == 0 or len(pes_sobrenome.strip()) == 0:
        messages.add_message(request, constants.ERRO, 'Email ou nome não pode ser vazio')
        return redirect('/auth/cadastro')
    
    if len(pes_senha) < 8:
        messages.add_message(request, constants.ERRO, 'Sua senha deve ter no mínimo 8 caracteres')
        return redirect('/auth/cadastro')
    
    if User.objects.filter(pes_email = pes_email).exists():
        messages.add_message(request, constants.ERRO, 'Já existe um usuário com esse e-mail')
        return redirect('/auth/cadastro')
    
    try:
        usuario = User.objects.create_user(user_name = pes_nome, last_name = pes_sobrenome, email = pes_email, password = pes_senha)
        usuario.save()
        return redirect('/auth/cadastro')
    
    except Exception as e:
        print(e)
        return redirect('/auth/cadastro')