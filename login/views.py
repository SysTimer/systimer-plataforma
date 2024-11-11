from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.messages import constants
from django.views.decorators.csrf import csrf_exempt
from .models import Pessoa, Empresa
import bcrypt
from django.db import transaction
from django.contrib.auth import get_user_model, authenticate
User = get_user_model()

def login(request):
    
    if request.user.is_authenticated:
        return redirect('/plataforma')
    
    status = request.GET.get('status', None)
    return render(request,'login.html', {'status': status})

def cadastro(request):
    status = request.GET.get('status', None)
    return render(request, 'cadastro.html', {'status': status})

@csrf_exempt
def validar_login(request):
    pes_email = request.POST.get('email')
    pes_senha = request.POST.get('password')
    print('Email -> ', pes_email, ' Senha -> ',  pes_senha)
    usuario = auth.authenticate(request, username=pes_email, password=pes_senha)
    print('Login -> ', usuario)
    if usuario is not None:
        auth.login(request, usuario)
        return redirect('/plataforma')
    
    return redirect('/auth/login')

    # usuario = auth.authenticate(request, username=pes_email, password=pes_senha)
    # print(usuario)
    # if usuario is None:
    #     messages.add_message(request, constants.WARNING, 'Email ou senha inválidos')
    #     return redirect('/auth/login')
    
   
    # return redirect('/plataforma')
    
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
    
    # elif User.objects.filter(email=pes_email).exists():
    #     messages.add_message(request, constants.WARNING, 'Já existe um usuário com esse e-mail')
    #     return redirect('/auth/cadastro')
    
    # elif User.objects.filter(username=pes_nome).exists():
    #     messages.add_message(request, constants.WARNING, 'Já existe um usuário ou empresa com esse nome')
    #     return redirect('/auth/cadastro')
    
    try:
        senha_codificada = bcrypt.hashpw( pes_senha.encode('UTF-8'), bcrypt.gensalt())
        print('Senha - > ', senha_codificada.decode('UTF-8'))
        
        with transaction.atomic():
            usuario = Pessoa(
                PES_NOME=pes_nome, 
                PES_SOBRENOME=pes_sobrenome, 
                PES_EMAIL=pes_email, 
                password=senha_codificada.decode('UTF-8')
            )
            usuario.save()
            print('Usuário salvo com sucesso!')
        
        with transaction.atomic():
            empresa = Empresa(
                EMP_NOME=emp_nome, 
                PES_COD=usuario  # Relacionamento com o usuário criado
            )
            empresa.save()
            print('Empresa salva com sucesso!')
        
        print('Usuário salvo com sucesso!')
        return redirect('/auth/cadastro')
    
    except Exception as e:
        print(e)
        return redirect('/auth/cadastro')

