import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Projeto, EmpresaPessoaView, Empresa, Pessoa
from login.models import LoginAuditoria
from django.http import HttpResponse
from django.utils import timezone


@login_required()
def response(request):
    print('response > ', request)
    return render("base.html", {'variavel': {"TESTE"}})

@login_required(login_url='/auth/login')
def plataforma(request):
    codigo_logado = request.user.PES_COD
    empresas = EmpresaPessoaView.objects.filter(pes_cod=codigo_logado)

    for i in empresas:
        print(i.pes_nome)


    if empresas is None: 
        retorno = {
            'status': 'ALERT',
            'Msg': 'Não encontramos nenhuma empresa associado a seu usuário'
        }
    else : 
        retorno = {
            'status': 'OK',
            'empresas': empresas
        }
    
    
    return render(request, 'empresa.html', retorno)
    
@login_required(login_url='/auth/login')
def sair(request):
    logout(request)
    return redirect('/auth/login')

@login_required
def renderizar_cadastro(request):
    return render(request, 'projeto.html')

@login_required
def cadastro_projeto(request):
    nome_projeto = request.POST.get('nome_projeto')

    if nome_projeto is not None:
        # Retornar Error...
        return render('')    
    
    meu_projeto = Projeto()

    return 0 


@login_required()
def selecionar_empresa(request):
    emp_cod = request.POST.get('emp_cod')
    emp_cargo = request.POST.get('cargo_nome')

    if emp_cod is None or emp_cargo is None: 
        # colocar msg de que precisar selecionar alguma empresa la da listin
        return HttpResponse({'sem nome do cargo ou empressa'}); 
    

    codigo_logado = request.user.PES_COD
    
    pessoa = Pessoa.objects.get(PES_COD=codigo_logado)
    empresa = Empresa.objects.get(EMP_COD=emp_cod)
    
    login_auditoria = LoginAuditoria(pes_cod = pessoa, emp_cod  = empresa, la_data_ultima = datetime.datetime.now())
    print(login_auditoria)
    login_auditoria.save()

    
    request.session['emp_cod'] = emp_cod
    request.session['cargo'] = emp_cargo
    return redirect('/plataforma/home')


@login_required
def renderizar_plataforma(request):
    print(timezone.now())
    empresa_codigo = request.session.get('emp_cod')
    
    if empresa_codigo is None:
        # avisar ao usuário que falhou ao bter a empresa dele e redirecionar ele para a tela de empresas.
        return redirect('plataforma/')
    
    empresa = Empresa.objects.filter(EMP_COD = empresa_codigo)
    
    if empresa: 
        retorno = {
            'status': "OK",
            
        }
    
    return render(request, 'home.html')