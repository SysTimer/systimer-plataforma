from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.messages import constants
from django.views.decorators.csrf import csrf_exempt
from .models import Pessoa, Empresa, PessoaToken
from django.db import transaction
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
import secrets
from plataforma.models import Funcionario, Cargo
from django.http import HttpResponse
from django.utils import timezone
from datetime import datetime, timedelta
from django.shortcuts import render, get_object_or_404

User = get_user_model()

def login(request):
    messages.add_message(request, constants.INFO, 'Bem-vindo ao sistema!')
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

def validar_cadastro(request):  
    print('Olá mundo entroui aqui sim')
    pes_nome = request.POST['pes_nome']
    pes_sobrenome = request.POST['pes_sobrenome']
    pes_email = request.POST['pes_email']
    pes_senha = request.POST['pes_senha']
    emp_nome = request.POST['emp_nome']
        
    # if len(pes_nome.strip()) == 0 or len(pes_email.strip()) == 0 or len(pes_sobrenome.strip()) == 0 or len(emp_nome.strip()) == 0:
    #     messages.add_message(request, constants.WARNING, 'Email, nome, Sobrenome ou Empresa não podem ser vazio')
    #     return redirect('/auth/cadastro')
    
    # elif len(pes_senha) < 8:
    #     messages.add_message(request, constants.WARNING, 'Sua senha deve ter no mínimo 8 caracteres')
    #     return redirect('/auth/cadastro')
    
    # elif User.objects.filter(email=pes_email).exists():
    #     messages.add_message(request, constants.WARNING, 'Já existe um usuário com esse e-mail')
    #     return redirect('/auth/cadastro')
    
    # elif User.objects.filter(username=pes_nome).exists():
    #     messages.add_message(request, constants.WARNING, 'Já existe um usuário ou empresa com esse nome')
    #     return redirect('/auth/cadastro')
    print(request.POST)
    try:
        senha_codificada = make_password(pes_senha)
        
        with transaction.atomic():
            usuario = Pessoa(
                PES_NOME=pes_nome, 
                PES_SOBRENOME=pes_sobrenome, 
                PES_EMAIL=pes_email, 
                PES_ADMINISTRADOR = 'S',
                password=senha_codificada
            )
            usuario.save()
        
        with transaction.atomic():
            empresa = Empresa(
                EMP_NOME=emp_nome, 
                PES_COD=usuario 
            )
            empresa.save()
           
        cargo  =  Cargo.objects.filter(CARGO_NOME = 'Administrador').first()
         
        if cargo is None:
            cargo = Cargo(CARGO_NOME = 'Administrador')
            cargo.save()
        

        with transaction.atomic():
            funcionario = Funcionario(PES_COD = usuario, EMP_COD = empresa, FUN_ROLES = cargo)
            funcionario.save()
        
        pessoa_login = Pessoa.objects.filter(PES_EMAIL = pes_email, PES_NOME = pes_nome).first()
        usuario = auth.authenticate(request, username=pes_email, password=pes_senha)
        
        request.session['emp_cod'] = empresa.EMP_COD
        request.session['cargo'] = cargo.CARGO_NOME
        auth.login(request, usuario)
        return redirect('/plataforma/home/')
    except Exception as e:
        print('Exceção causada > ', e)
        return redirect('/auth/cadastro')

def recuperar_senha(request):    
    return render(request, 'recuperar_senha.html')

def validar_token(request):
    print('CAIU AQUI')
    print(request.GET)
    token = request.GET.get('token')
    senha = request.POST.get('senha')
    
    print('Info> ', token, senha)

    token_usuario = PessoaToken.objects.filter(PST_TOKEN=token, PST_EXPIRADO = 'N')
    
    if token_usuario.exists():
        token_instance = token_usuario[0]
        data_atual = timezone.now()
        if token_instance.PST_DATA_EXPIRACAO >= data_atual:
            pessoa_tk = token_usuario.first()
            pessoa_senha = Pessoa.objects.filter(PES_COD= token_instance.PES_COD_id).first()
            pessoa_senha.password = make_password(senha)
            token_instance.PST_EXPIRADO = 'S'
            pessoa_senha.save()
            token_instance.save()
            return redirect('login')
        else:
            return redirect('login')   
    return HttpResponse('Falha na comunicação')


def recuperar_acesso(request):
    email = request.POST.get('recuperar_email')
    usuario = Pessoa.objects.filter(PES_EMAIL = email)
    
    if usuario.exists():
        usuario_instancia = usuario[0]
        token = secrets.token_hex(2)
        data_expiracao = datetime.now() + timedelta(minutes=15)
        pessoa_token = PessoaToken(PES_COD = usuario_instancia, PST_TOKEN = token, PST_DATA_EXPIRACAO = data_expiracao)
        pessoa_token.save()
        messages.add_message(request, constants.SUCCESS, 'Verifique sua caixa de entrada no e-mail')
        return redirect('/auth/login')
    return redirect('/auth/login')

def update_view(request):
    email = request.GET.get('email')
    token = request.GET.get('token')
    
    # Pedro colocar messages no if e adicioanr try catch

    if not email or not token:
        return render(request, 'error.html', {'message': 'Email ou token não fornecido.'})

    pessoa = get_object_or_404(Pessoa, PES_EMAIL=email)

    if pessoa.PES_TOKEN != token: 
        return render(request, 'error.html', {'message': 'Token inválido.'})

    if pessoa.PES_CADASTRO_COMPLETO == 'N':
        funcionario_instancia = Funcionario.objects.select_related('EMP_COD').filter(PES_COD=pessoa).first()
        nome_empresa = funcionario_instancia.EMP_COD.EMP_NOME
        
        retorno = {
            "pessoa": pessoa,
            "nome_empresa": nome_empresa,
            'email': email,
            'token': token,
        }

        return render(request, 'confirmar_conta.html', retorno)
    else:
        return redirect('/auth/login/')
    
def update_view_funcionario(request):
    email = request.GET.get('email')
    token = request.GET.get('token')
    
    print('Email -> ', email)

    # Pedro colocar messages no if e adicioanr try catch

    if not email or not token:
        return render(request, 'error.html', {'message': 'Email ou token não fornecido.'})

    pessoa = get_object_or_404(Pessoa, PES_EMAIL=email)
    funcionario = get_object_or_404(Funcionario, FUN_TOKEN = token, PES_COD = pessoa.PES_COD)
    


    if funcionario.FUN_TOKEN != token: 
        return render(request, 'error.html', {'message': 'Token inválido.'})

    if funcionario.FUN_APROVADO == 'N':
        nome_empresa = funcionario.EMP_COD.EMP_NOME
        
        retorno = {
            "pessoa": pessoa,
            "nome_empresa": nome_empresa,
            'email': email,
            'token': token,
        }

        return render(request, 'confirmar_conta _funcionario.html', retorno)
    else:
        return redirect('/auth/login/')


def update_password(request):
    email = request.POST.get('email')
    token = request.POST.get('token')
    nova_senha = request.POST.get('nova_senha')
    pessoa = get_object_or_404(Pessoa, PES_EMAIL=email, PES_TOKEN = token)
    if not pessoa:
        # pedro colocar msg dizenod que n foi encontrado a pessoa
        return redirect('/auth/login/')
    
    funcionario_instancia = Funcionario.objects.filter(PES_COD = pessoa.PES_COD).first()

    funcionario_instancia.FUN_APROVADO = 'S'
    pessoa.password = nova_senha
    pessoa.PES_CADASTRO_COMPLETO = 'S'
    pessoa.save()
    funcionario_instancia.save();
    return redirect('/auth/login/')



def update_funcionario(request):
    
    email = request.POST.get('email')
    token = request.POST.get('token')
    
    pessoa = get_object_or_404(Pessoa, PES_EMAIL=email)
    funcionario = get_object_or_404(Funcionario, PES_COD = pessoa.PES_COD, FUN_TOKEN = token)
    print('Funcionario -> ', funcionario)
    if not funcionario:
        # pedro colocar msg dizenod que n foi encontrado a pessoa
        return redirect('/auth/login/')
    funcionario.FUN_APROVADO = 'S'
    funcionario.save();
    # Quando for sucesso, redirecione para o login com mensagem dizendo que ele foi aprovado com sucesso e precisa faazer
    # Login para continuar 
    return redirect('/auth/login/')
