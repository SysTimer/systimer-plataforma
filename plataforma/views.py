import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Projeto, EmpresaPessoaView, Empresa, Pessoa, HorasTarefasVI, Tarefas,  Horas_Trabalhadas
from login.models import LoginAuditoria
from django.http import JsonResponse, HttpResponse


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
    empresa_codigo = request.session.get('emp_cod')
    pes_cod_id = request.user.PES_COD
    if empresa_codigo is None:
        # avisar ao usuário que falhou ao bter a empresa dele e redirecionar ele para a tela de empresas.
        return redirect('plataforma/')
    
    try:
        empresa = Empresa.objects.filter(EMP_COD = empresa_codigo)
        minhas_tarefas = HorasTarefasVI.objects.filter(emp_cod_id = empresa_codigo, pes_cod = pes_cod_id)
    
    

        if empresa: 
            retorno = {
                'status': "OK",
                
            }
            
        retorno  = {
            "minhas_tarefas": minhas_tarefas
        }
        return render(request, 'home.html', retorno)
    except Exception as e:
        return HttpResponse(e); 




@login_required

def iniciar_tarefa(request):
    trf_cod  = request.POST.get('trf_cod')
    pes_cod = request.user.PES_COD
    emp_cod = request.session.get('emp_cod')
    if trf_cod is None:
        return JsonResponse({'status': 'alert', 'msg': 'Não foi possivel iniciar a tarefa'}, status=202)
    
    verificar_tarefa = Tarefas.objects.filter(PES_COD=pes_cod).filter(TRF_COD=trf_cod).first()  

    if verificar_tarefa is  None:
        print('Entrou aqui')
        return JsonResponse({'status': 'ERROR', 'Msg': 'Não permitido'}, status=202)
    
    minha_tarefa = Tarefas.objects.filter(TRF_COD = trf_cod).first()
    pessoa = Pessoa.objects.filter(PES_COD = pes_cod).first()
    data = datetime.datetime.now()


    horas_existente = Horas_Trabalhadas.objects.filter(
    TRF_COD=minha_tarefa,
    PES_COD=pessoa,
    HRT_DT_FIM__isnull=True
    ).first()       
    
    if horas_existente:
        horas_existente.HRT_DT_FIM = data
        horas_existente.save()
    else: 
        
        tarefa_inicia_existente = Horas_Trabalhadas.objects.filter(PES_COD = pes_cod, HRT_DT_FIM__isnull=True ).first()
    
        if tarefa_inicia_existente:
            tarefa_inicia_existente.HRT_DT_FIM = data;
            tarefa_inicia_existente.save()

        minhas_horas = Horas_Trabalhadas(HRT_DT_INICIO = data, PES_COD = pessoa, TRF_COD = minha_tarefa)
        minhas_horas.save()
        
    return JsonResponse({'status': 'OK', 'Msg': 'Iniciado com Sucesso'}, status=202)

    