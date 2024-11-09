from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.contrib.messages import constants
from django.views.decorators.csrf import csrf_exempt

def login(request):
    status = request.GET.get('status', None)
    return render(request,'login.html', {'status': status})

def cadastro(request):
    status = request.GET.get('status', None)
    return render(request, 'cadastro.html', {'status': status})

@csrf_exempt
def validar_login(request):
    pes_email = request.POST.get('email')
    pes_senha = request.POST.get('password')
    
    usuario = auth.authenticate(request, username=pes_email, password=pes_senha)
    print(usuario)
    if usuario is None:
        messages.add_message(request, constants.WARNING, 'Email ou senha inválidos')
        return redirect('/auth/login')
    
    auth.login(request, usuario)
    return redirect('/plataforma/home')
    
def validar_cadastro(request):  
    pes_nome = request.POST['pes_nome']
    pes_sobrenome = request.POST['pes_sobrenome']
    pes_email = request.POST['pes_email']
    pes_senha = request.POST['pes_senha']
    emp_nome = request.POST['emp_nome']
    
    print(request.POST)
    
    if len(pes_nome.strip()) == 0 or len(pes_email.strip()) == 0 or len(pes_sobrenome.strip()) == 0 or len(emp_nome.strip()) == 0:
        messages.add_message(request, constants.WARNING, 'Email, nome, Sobrenome ou Empresa não podem ser vazio')
        return redirect('/auth/cadastro')
    
    elif len(pes_senha) < 8:
        messages.add_message(request, constants.WARNING, 'Sua senha deve ter no mínimo 8 caracteres')
        return redirect('/auth/cadastro')
    
    elif User.objects.filter(email=pes_email).exists():
        messages.add_message(request, constants.WARNING, 'Já existe um usuário com esse e-mail')
        return redirect('/auth/cadastro')
    
    elif User.objects.filter(username=pes_nome).exists():
        messages.add_message(request, constants.WARNING, 'Já existe um usuário ou empresa com esse nome')
        return redirect('/auth/cadastro')
    
    try:
        usuario = User.objects.create_user(username=pes_nome, last_name=pes_sobrenome, email=pes_email, password=pes_senha)
        usuario.save()
        print('Usuário salvo com sucesso!')
        return redirect('/auth/cadastro')
    
    except Exception as e:
        print(e)
        return redirect('/auth/cadastro')
