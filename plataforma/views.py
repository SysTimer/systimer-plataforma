import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Projeto, EmpresaPessoaView, Empresa, Pessoa, HorasTarefasVI, Tarefas,  Horas_Trabalhadas, SysDetalhesTarefasVi,Horas_Reprovadas, Prioridade, Funcionario, Projeto, Cliente
from login.models import LoginAuditoria
from django.http import JsonResponse, HttpResponse
from django.contrib import messages


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
    login_auditoria.save()

    
    request.session['emp_cod'] = emp_cod
    request.session['cargo'] = emp_cargo
    return redirect('/plataforma/home')


@login_required
def renderizar_plataforma(request):
    empresa_codigo = request.session.get('emp_cod')
    pes_cod_id = request.user.PES_COD
    if empresa_codigo is None:
        return redirect('plataforma/')
    
        
    funcionario = Funcionario.objects.filter(PES_COD =  pes_cod_id).first()
    
    print(funcionario)
        
    empresa = Empresa.objects.filter(EMP_COD = empresa_codigo)
    minhas_tarefas = HorasTarefasVI.objects.filter(emp_cod_id = empresa_codigo, fun_cod = funcionario.FUN_COD)
    tarefas_pendentes = SysDetalhesTarefasVi.objects.filter(trf_status='P', fun_cod=funcionario.FUN_COD)
    tarefas_reprovadas = SysDetalhesTarefasVi.objects.filter(trf_status='R', fun_cod=funcionario.FUN_COD)
    tarefas_aprovadas = SysDetalhesTarefasVi.objects.filter(trf_status='AP', fun_cod=funcionario.FUN_COD)


    if empresa: 
        retorno = {
            'status': "OK",
                
        }
            
    retorno  = {
         "minhas_tarefas": minhas_tarefas,
         "trf_pendente": tarefas_pendentes,
        "tarefas_reprovadas": tarefas_reprovadas,
        "quantidade_pendente": tarefas_pendentes.count(),
        "tarefas_aprovadas": tarefas_aprovadas,
    }
    return render(request, 'home.html', retorno)




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


@login_required
def enviar_banco_horas(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Método não permitido.'}, status=405)

    trf_cod = request.POST.get('trf_cod')
    trf_acao = request.POST.get('trf_acao')
    pes_cod = request.user.PES_COD
    

    if not pes_cod:
        return JsonResponse({'status': 'ERROR', 'Msg': 'Usuário não localizado'}, status=401)
    if not trf_cod:
        return JsonResponse({'status': 'ERROR', 'Msg': 'Tarefa não localizada'}, status=404)
    if not trf_acao:
        return JsonResponse({'status': 'ERROR', 'Msg': 'Ação não localizada'}, status=404)

    try:
        horas_existente = Tarefas.objects.filter(PES_COD_id=pes_cod, TRF_COD=trf_cod).first()
        if not horas_existente:
            return JsonResponse({'status': 'ERROR', 'Msg': 'Usuário não autorizado a modificar a tarefa'}, status=401)
        data = datetime.datetime.now()

        if trf_acao in ['P', 'AR', 'R']:
           horas_existente.TRF_STATUS = trf_acao
           horas_existente.TRF_DATA_CONCLUSAO =  data
           horas_existente.save()
           return JsonResponse({'status': 'OK', 'Msg': 'Tarefa modificada com sucesso'}, status=202)
        else:
            return JsonResponse({'status': 'ERROR', 'Msg': 'Ação inválida'}, status=400)

    except Exception as e:
        # Tratamento genérico para exceções
        return JsonResponse({'status': 'ERROR', 'Msg': f'Erro interno: {str(e)}'}, status=500)


    
    
    
@login_required
def atualizar_registro(request):
    trf_cod = request.POST.get('trf_cod')
    justificativa =  request.POST.get('justificativa')
    pes_cod = request.user.PES_COD

    print('trf_cod -> ', trf_cod, ' justify ->', justificativa)

    if trf_cod is None or pes_cod is None:
        return HttpResponse("ERRO")

    
    tarefa = Tarefas.objects.filter(TRF_COD = trf_cod, PES_COD = pes_cod).first()
    data = datetime.datetime.now()

    if tarefa:
        hr_reprovada = Horas_Reprovadas(HRR_DT_ULTIMA = data ,HRR_JUSTIFICATIVA = justificativa, TRF_COD = tarefa )
        hr_reprovada.save()
        tarefa.TRF_STATUS = 'R'
        tarefa.save()
        return redirect('/')
    else: 
        return HttpResponse("ERRO  TRESTE")

         


@login_required
def renderizar_cadastro(request):
    cargo = request.session.get('cargo')
    usuario = request.user
    emp_cod = request.session.get('emp_cod')
    
    try:
        funcionario = Funcionario.objects.filter(PES_COD=usuario.PES_COD).first()
        empresa = funcionario.EMP_COD
    except Funcionario.DoesNotExist:
        empresa = None

    projetos = Projeto.objects.filter(CLI_COD__EMP_COD=emp_cod) 
    prioridades = Prioridade.objects.all()

    print(funcionario.PES_COD.PES_COD)
    
    if cargo == 'Dono': 
        funcionarios = Funcionario.objects.all()
    else:
        funcionarios = Funcionario.objects.filter(PES_COD=usuario.PES_COD)

    clientes = Cliente.objects.filter(EMP_COD=emp_cod) if empresa else Cliente.objects.all()

    return render(request, 'cadastrar_tarefa.html', {
        'projetos': projetos,
        'prioridades': prioridades,
        'funcionarios': funcionarios,
        'clientes': clientes,
        'cargo': cargo
    })
    
    
def projetos_clientes(request):
    cliente_cod = request.GET.get('cliente_cod')
    
    if cliente_cod:
        projetos = Projeto.objects.filter(CLI_COD=cliente_cod).values('PJT_COD', 'PJT_NOME')
        projetos_list = list(projetos)
        
        return JsonResponse({'projetos': projetos_list})
    else:
        return JsonResponse({'error': 'Cliente não especificado'}, status=400)
    
    
    
@login_required
def cadastrar_tarefa(request):
    
    cliente = request.POST.get('cliente')
    projeto = request.POST.get('projeto')
    prioridade = request.POST.get('prioridade')
    funcionario = request.POST.get('funcionario')
    titulo = request.POST.get('titulo')
    observacao = request.POST.get('obs')

     # Pedro - Adicionar Django Message!
    if not cliente or not projeto:
        messages.error(request, 'Cliente ou projeto não pode ser vazio!')
    elif not funcionario:
        messages.warning(request, 'Funcionário não selecionado!')
    elif not prioridade:
        messages.warning(request, 'Prioridade não selecionado!')

    projeto_instancia = Projeto.objects.filter(PJT_COD = projeto).first()
    prioridade_instancia = Prioridade.objects.filter(PRI_COD = prioridade).first()
    funcionario_instancia = Funcionario.objects.filter(FUN_COD = funcionario).first()
    
    
    tarefa_instancia = Tarefas(PJT_COD = projeto_instancia, TRF_TITULO = titulo, FUN_COD = funcionario_instancia, TRF_PRIORIDADE =  prioridade_instancia, TRF_OBSERVACAO = observacao)
    tarefa_instancia.save()
    
    return redirect('/plataforma/home')
    
    
    
@login_required    
def novo_projeto(request):
    emp_cod = request.session.get('emp_cod'); 
    
    if emp_cod is None:
        return HttpResponse('Erro') # Dps trocar para o alert do django mssgae
        
    
    clientes = Cliente.objects.filter(EMP_COD = emp_cod).values('CLI_COD', 'CLI_NOME')
    
    retorno = {
        "cliente": clientes
    }
    
    return render (request, 'novo_projeto.html', retorno)

