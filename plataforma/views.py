import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Projeto, EmpresaPessoaView, Empresa, Pessoa, HorasTarefasVI, Tarefas,  Horas_Trabalhadas, Cliente, SysDetalhesTarefasVi,Horas_Reprovadas, Prioridade, Funcionario, Projeto, Cliente, EmpresaInfo,SysGraficosHorasVi,SysEquipeVi

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
    
        
    empresa = Empresa.objects.filter(EMP_COD = empresa_codigo).first()
    minhas_tarefas = HorasTarefasVI.objects.filter(emp_cod_id = empresa_codigo, fun_cod = funcionario.FUN_COD)
    tarefas_pendentes = SysDetalhesTarefasVi.objects.filter(trf_status='P', fun_cod=funcionario.FUN_COD)
    tarefas_reprovadas = SysDetalhesTarefasVi.objects.filter(trf_status='R', fun_cod=funcionario.FUN_COD)
    tarefas_aprovadas = SysDetalhesTarefasVi.objects.filter(trf_status='AP', fun_cod=funcionario.FUN_COD)
            
    for tarefa in tarefas_pendentes:
     print(tarefa)    
            
            
    retorno  = {
         "minhas_tarefas": minhas_tarefas,
         "trf_pendente": tarefas_pendentes,
        "tarefas_reprovadas": tarefas_reprovadas,
        "quantidade_pendente": tarefas_pendentes.count(),
        "tarefas_aprovadas": tarefas_aprovadas,
        "empresa_nova": empresa.EMP_NOVO
    }
    return render(request, 'home.html', retorno)




@login_required
def iniciar_tarefa(request):
    trf_cod  = request.POST.get('trf_cod')
    pes_cod = request.user.PES_COD
    emp_cod = request.session.get('emp_cod')
    if trf_cod is None:
        return JsonResponse({'status': 'alert', 'msg': 'Não foi possivel iniciar a tarefa'}, status=202)
    
    funcionario_instancia = Funcionario.objects.filter(PES_COD = pes_cod).first()

    verificar_tarefa = Tarefas.objects.filter(FUN_COD = funcionario_instancia.FUN_COD).filter(TRF_COD=trf_cod).first()  

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
        funcionario_instancia = Funcionario.objects.filter(PES_COD = pes_cod).first()
        horas_existente = Tarefas.objects.filter(FUN_COD = funcionario_instancia.FUN_COD, TRF_COD=trf_cod).first()
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
        return JsonResponse({'status': 'ERROR', 'Msg': f'Erro interno: {str(e)}'}, status=500)


    
    
    
@login_required
def atualizar_registro_reprovada(request):
    trf_cod = request.POST.get('trf_cod')
    justificativa =  request.POST.get('justificativa')
    pes_cod = request.user.PES_COD

    if trf_cod is None or pes_cod is None:
        return JsonResponse({'status': 'ERROR', 'Msg': 'Tarefa inválida ou usuário inválido'}, status=401)

    funcionario_instancia = Funcionario.objects.filter(PES_COD = pes_cod).first()
    tarefa = Tarefas.objects.filter(TRF_COD = trf_cod, FUN_COD = funcionario_instancia.FUN_COD).first()
    data = datetime.datetime.now()

    if tarefa:
        hr_reprovada = Horas_Reprovadas(HRR_DT_ULTIMA = data ,HRR_JUSTIFICATIVA = justificativa, TRF_COD = tarefa )
        hr_reprovada.save()
        tarefa.TRF_STATUS = 'R'
        tarefa.save()
        return redirect('/plataforma/home/')
    else: 
        return JsonResponse({'status': 'ERROR', 'Msg': 'Não autorizado'}, status=401)    
         
@login_required
def atualizar_registro_aprovada(request):
    trf_cod = request.POST.get('trf_cod')
    pes_cod = request.user.PES_COD
    print(request.POST)

    if trf_cod is None or pes_cod is None:
        return JsonResponse({'status': 'ERROR', 'Msg': 'Tarefa inválida ou usuário inválido'}, status=401)


    funcionario_instancia = Funcionario.objects.filter(PES_COD = pes_cod).first()
    tarefa = Tarefas.objects.filter(TRF_COD = trf_cod, FUN_COD = funcionario_instancia.FUN_COD).first()
    
    if tarefa:
        tarefa.TRF_STATUS = 'AP'
        tarefa.save()
        return redirect('/plataforma/home/')
    else: 
        return JsonResponse({'status': 'ERROR', 'Msg': 'Não autorizado'}, status=401)    


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
    if cargo == 'Administrador': 
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
def exibir_grafico(request):
    trf_cod = request.GET.get('tarefa')
    pes_cod = request.user.PES_COD
    
    dados_instancia = SysGraficosHorasVi.objects.filter(TRF_COD_id = trf_cod, PES_COD_id = pes_cod)
    
    retorno = {
        "dados": dados_instancia
    }
    
    return render(request,'analisar.html', retorno)
    
    
@login_required
def cadastrar_tarefa(request):
    
    print(request.POST)
    
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


@login_required
def cadastrar_informacoes(request):
    tamanho = request.POST.get('tamanho')
    nome_cliente = request.POST.get('nome_cliente')
    nome_projeto = request.POST.get('nome_projeto')
    atuacao = request.POST.get('area')
    emp_cod = request.session.get('emp_cod')

    
    if not tamanho or not nome_cliente or not nome_projeto:
        # PEDRO FAZER AQUI TAMBÉM, E RETORNAR ERRO LA NO FORM
        return HttpResponse('Teste')
    
    try:
        empresa_instancia = Empresa.objects.filter(EMP_COD = emp_cod ).first()
        
        if empresa_instancia:
            
            empresa_instancia.EMP_NOVO = 'N'
            empresa_info = EmpresaInfo(EMP_QUANTIDADE_FUNC = tamanho, EMP_RAMO_ATUACAO = atuacao, EMP_COD = empresa_instancia )
            
            cliente_novo = Cliente(CLI_NOME = nome_cliente, EMP_COD = empresa_instancia)
            cliente_novo.save()
            
            projeto = Projeto(PJT_NOME = nome_projeto, CLI_COD = cliente_novo) 
            projeto.save()
            empresa_info.save()
            empresa_instancia.save()
            return redirect('/plataforma/home/')
        else: 
            # PEDRO FAZER AQUI TAMBÉM, E RETORNAR ERRO LA NO FORM
            return HttpResponse('Retornar o erro para usuário') 
    except Exception as e: 
        print(e)
        return HttpResponse('Retornar o erro para usuário') 
    
    

@login_required
def criar_cliente(request):
    nome_cliente = request.POST.get('nome_cliente')
    emp_cod = request.session.get('emp_cod')

    empresa_instancia = Empresa.objects.filter(EMP_COD=emp_cod).first()
    
    # Cria e salva o cliente
    cliente = Cliente(CLI_NOME=nome_cliente, EMP_COD=empresa_instancia)
    cliente.save()

    referer_url = request.META.get('HTTP_REFERER', '')
    
    if '/plataforma/renderizar_cadastro/' in referer_url:
        return redirect('/plataforma/renderizar_cadastro/')
    elif '/plataforma/novo_projeto/' in referer_url:
        return redirect('/plataforma/novo_projeto/')
    


@login_required
def editar_usuario(request):
    pes_cod = request.user.PES_COD
    pessoa = Pessoa.objects.filter(PES_COD=pes_cod).first()

    if pessoa:
        if request.method == 'POST':
            nome = request.POST.get('nome')
            sobrenome = request.POST.get('sobrenome')
            email = request.POST.get('email')
            foto = request.FILES.get('foto')
            senha = request.POST.get('senha')
            cargo = request.POST.get('cargo')

            pessoa.PES_NOME = nome
            pessoa.PES_SOBRENOME = sobrenome
            pessoa.PES_EMAIL = email

            if foto:
                pessoa.foto = foto
            if senha:
                pessoa.set_password(senha)
            pessoa.cargo = cargo

            pessoa.save()

            return redirect('perfil_usuario')

        return render(request, 'editar_usuario.html', {'pessoa': pessoa})

    return redirect('login')

    
@login_required    
def salvar_perfil(request):
    
    pes_cod = request.user.PES_COD
    
    
    pessoa = Pessoa.objects.filter(PES_COD=pes_cod).first()
    
    if pessoa:
        
        if request.method == 'POST':
            novo_nome = request.POST.get('nome')
            novo_sobrenome = request.POST.get('sobrenome')
            
            pessoa.nome = novo_nome
            pessoa.sobrenome = novo_sobrenome
        
            pessoa.save()
            
            
            return redirect('perfil')  
        else:
            
            return render(request, 'editar_usuario.html', {'pessoa': pessoa})
    else:
        
        return redirect('login')

@login_required
def criar_projeto(request):
    cliente = request.POST.get('cliente')
    nome_projeto = request.POST.get('nome_projeto')     
    valor_hora = request.POST.get('valor_hora')
    notas = request.POST.get('notas')
    print(request.POST)
    if not cliente or not nome_projeto or not valor_hora:
            print("Erro: Todos os campos obrigatórios devem ser preenchidos!")
            return redirect('/plataforma/novo_projeto/')

    cliente_instancia = Cliente.objects.filter(CLI_COD = cliente).first()
    if cliente_instancia: 
        try:
            projeto_instancia = Projeto(PJT_NOME = nome_projeto, CLI_COD = cliente_instancia, PJT_VLR_HORA = valor_hora, PJT_OBSERVACAO = notas)
            projeto_instancia.save()  
            return redirect('/plataforma/novo_projeto/')
        except Exception as e:
            print(e)
            return redirect('/plataforma/novo_projeto/')

    else:
        print("Erro interno: Não foi possível inserir esse projeto no cleinte atual.")
        return redirect('/plataforma/novo_projeto/')


@login_required
def listar_projeto(request):
    
    # Agrupar os projetos por cliente
    projetos_com_clientes = Projeto.objects.select_related('CLI_COD').values('CLI_COD__CLI_NOME').distinct()
    projetos_por_cliente = {}

    for cliente in projetos_com_clientes:
        cli_nome = cliente['CLI_COD__CLI_NOME']
        projetos_por_cliente[cli_nome] = Projeto.objects.filter(CLI_COD__CLI_NOME=cli_nome).values('PJT_NOME')

    retorno = {
        "projetos_por_cliente": projetos_por_cliente
    }

    return render(request, 'projeto.html', retorno)


def renderizar_equipe(request):

    emp_cod = request.session.get('emp_cod')

    equipe = SysEquipeVi.objects.filter(emp_cod_id = emp_cod)
    
    retorno = {
       "equipe": equipe,
       "existe":  equipe.exists()     
    }
    

    return render(request, 'equipe.html', retorno)

def cadastrar_funcionario(request):
    return render(request, 'funcionario_novo.html')
