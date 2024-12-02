import datetime
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Horas_Aprovadas, Projeto, EmpresaPessoaView, Empresa, Invoice, Pessoa, HorasTarefasVI, Tarefas, Horas_Trabalhadas,FaturasPrevistaVI, Cliente, SysDetalhesTarefasVi,Horas_Reprovadas, Prioridade, Funcionario, Projeto, Cliente, EmpresaInfo,SysGraficosHorasVi,SysEquipeVi, Cargo
from login.models import LoginAuditoria
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.db.models import Q
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors

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

@login_required(login_url='/auth/login')
def renderizar_cadastro(request):
    return render(request, 'projeto.html')


@login_required(login_url='/auth/login')
def cadastro_projeto(request):
    nome_projeto = request.POST.get('nome_projeto')

    if nome_projeto is not None:
        # Retornar Error...
        return render('')    
    
    meu_projeto = Projeto()

    return 0 


@login_required(login_url='/auth/login')
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


@login_required(login_url='/auth/login')
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




@login_required(login_url='/auth/login')
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

@login_required(login_url='/auth/login')
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


    
    
    
@login_required(login_url='/auth/login/')
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
         
@login_required(login_url='/auth/login/')
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


@login_required(login_url='/auth/login/')
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
    
    
@login_required(login_url='/auth/login/')
def projetos_clientes(request):
    cliente_cod = request.GET.get('cliente_cod')
    
    if cliente_cod:
        projetos = Projeto.objects.filter(CLI_COD=cliente_cod).values('PJT_COD', 'PJT_NOME')
        projetos_list = list(projetos)
        
        return JsonResponse({'projetos': projetos_list})
    else:
        return JsonResponse({'error': 'Cliente não especificado'}, status=400)
    
    
@login_required(login_url='/auth/login/')
def exibir_grafico(request):
    trf_cod = request.GET.get('tarefa')
    pes_cod = request.user.PES_COD
    
    dados_instancia = SysGraficosHorasVi.objects.filter(TRF_COD_id = trf_cod, PES_COD_id = pes_cod, HRF_STATUS = 'A')
    
    if not dados_instancia:
        tarefa = Tarefas.objects.filter(TRF_COD  = trf_cod).first()
        tarefa.TRF_STATUS = 'F' # De finalizada
        tarefa.save()
        return redirect('/plataforma/home')
    
    
    retorno = {
        "dados": dados_instancia
    }
    
    return render(request,'analisar.html', retorno)
    
@login_required(login_url='/auth/login/')
def dados_graficos(request): 
    tarefa_codigo = request.GET.get('tarefa')
    
    faturas = FaturasPrevistaVI.objects.filter(TRF_COD_id=tarefa_codigo)
    
    faturas_list = list(faturas.values())
    
    retorno = {
        "retorno": faturas_list
    }
    
    return JsonResponse(retorno, status=202)
    
    
    

@login_required(login_url='/auth/login/')
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
    
    
    
@login_required(login_url='/auth/login/') 
def novo_projeto(request):
    emp_cod = request.session.get('emp_cod'); 
    
    if emp_cod is None:
        return HttpResponse('Erro') # Dps trocar para o alert do django mssgae
        
    
    clientes = Cliente.objects.filter(EMP_COD = emp_cod).values('CLI_COD', 'CLI_NOME')
    
    retorno = {
        "cliente": clientes
    }
    
    return render (request, 'novo_projeto.html', retorno)


@login_required(login_url='/auth/login/')
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
    
    

@login_required(login_url='/auth/login/')
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
    


@login_required(login_url='/auth/login/')
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

    
@login_required(login_url='/auth/login/')
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

@login_required(login_url='/auth/login/')
def criar_projeto(request):
    cliente = request.POST.get('cliente')
    nome_projeto = request.POST.get('nome_projeto')     
    valor_hora = request.POST.get('valor_hora')
    notas = request.POST.get('notas')
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


@login_required(login_url='/auth/login/')
def listar_projeto(request):
    
    projetos_com_clientes = Projeto.objects.select_related('CLI_COD').values('CLI_COD__CLI_NOME').distinct()
    projetos_por_cliente = {}

    for cliente in projetos_com_clientes:
        cli_nome = cliente['CLI_COD__CLI_NOME']
        projetos_por_cliente[cli_nome] = Projeto.objects.filter(CLI_COD__CLI_NOME=cli_nome).values('PJT_NOME')

    retorno = {
        "projetos_por_cliente": projetos_por_cliente
    }

    return render(request, 'projeto.html', retorno)

@login_required(login_url='/auth/login/')
def renderizar_equipe(request):

    emp_cod = request.session.get('emp_cod')

    equipe = SysEquipeVi.objects.filter(emp_cod_id = emp_cod)
    
    print('Equipe -> ', equipe.exists() )
    
    retorno = {
       "equipe": equipe,
       "existe":  equipe.exists()     
    }
    return render(request, 'equipe.html', retorno)

@login_required(login_url='/auth/login/')
def cadastrar_funcionario(request):
    
    emp_cod = request.session.get('emp_cod')
    cargos = Cargo.objects.filter(EMP_COD=emp_cod) | Cargo.objects.filter(EMP_COD__isnull=True)
    retorno = {
        "cargos": cargos
    }
    return render(request, 'funcionario_novo.html', retorno)

@login_required(login_url='/auth/login/')
def criar_cargo(request):
    emp_cod = request.session.get('emp_cod')
    if request.method == 'POST':
        nome_cliente = request.POST.get('nome_cliente')
        if nome_cliente:
            empresa_instancia = Empresa.objects.filter(EMP_COD = emp_cod).first()
            novo_cargo = Cargo(CARGO_NOME=nome_cliente, EMP_COD=empresa_instancia)
            novo_cargo.save()
            messages.success(request, 'Cliente adicionado com sucesso!')
            return redirect('/plataforma/cadastrar_funcionario')  
        else:
            messages.error(request, 'Por favor, forneça o nome do Cargo.')
    # Pedro ajeitar essse django message
    return redirect('/plataforma/cadastrar_funcionario')  

@login_required(login_url='/auth/login/')
def criar_funcionario(request):
    if request.method == 'POST':
        primeiro_nome = request.POST.get('primeiro_nome')
        sobrenome = request.POST.get('sobrenome')
        tipo_usuario = request.POST.get('tipo_usuario')
        cargo = request.POST.get('cargo')
        capacidade = request.POST.get('capacidade')
        valor_hora = request.POST.get('valor_hora')
        email = request.POST.get('email')
        emp_cod = request.session.get('emp_cod')

        pessoa_existe = Pessoa.objects.filter(PES_EMAIL=email).first()
        
        if pessoa_existe:
            
            funcionario_instancia = Funcionario.objects.filter(PES_COD = pessoa_existe.PES_COD)
        
            if funcionario_instancia:
                print('Funcionario ja existe!')
                # PEDRO COLOCAR AQ TBM
                return redirect('/plataforma/cadastrar_funcionario') 
            
            empresa_instacnia = Empresa.objects.filter(EMP_COD=emp_cod).first()
            cargo_instacnia = Cargo.objects.filter(CARGO_COD=cargo).first()
            
            token_aprovacao = get_random_string(32)


            novo_funcionario = Funcionario(
                PES_COD=pessoa_existe,
                EMP_COD=empresa_instacnia,
                FUN_ROLES=cargo_instacnia,
                FUN_MAXIMO_HORAS=capacidade,
                FUN_VALOR_HORA=valor_hora,
                FUN_APROVADO='N',
                FUN_TOKEN=token_aprovacao,
                FUN_TIPO = tipo_usuario
            )
            novo_funcionario.save()

           
            return redirect('/plataforma/equipe')  
        
        else:
            pes_token = get_random_string(32)

            nova_pessoa = Pessoa(
                PES_NOME=primeiro_nome,
                PES_SOBRENOME = sobrenome,
                PES_EMAIL=email,
                PES_TOKEN = pes_token,
                PES_CADASTRO_COMPLETO = 'N'
            )
            nova_pessoa.save()

            empresa_instacnia = Empresa.objects.filter(EMP_COD=emp_cod).first()
            cargo_instacnia = Cargo.objects.filter(CARGO_COD=cargo).first()

            token_aprovacao = get_random_string(32)

            novo_funcionario = Funcionario(
                PES_COD=nova_pessoa,
                EMP_COD=empresa_instacnia,
                FUN_ROLES=cargo_instacnia,
                FUN_MAXIMO_HORAS=capacidade,
                FUN_VALOR_HORA=valor_hora,
                FUN_APROVADO='N',
                FUN_TOKEN=token_aprovacao,
                FUN_TIPO = tipo_usuario
            )
            novo_funcionario.save()
        return redirect('/plataforma/equipe')  



    


@login_required(login_url='/auth/login/')
def obter_funcionario(request):
    fun_cod = request.GET.get('fun_cod')
    emp_cod = request.session.get('emp_cod')
    funcionario_instancia = Funcionario.objects.filter(FUN_COD=fun_cod).select_related('PES_COD', 'FUN_ROLES')

    if funcionario_instancia.exists():
        funcionario = funcionario_instancia.first()
        
        cargos = Cargo.objects.filter(
            Q(EMP_COD=emp_cod) | Q(EMP_COD__isnull=True)
        ).exclude(CARGO_NOME='Administrador').values('CARGO_COD', 'CARGO_NOME')

        
        response_data = {
            'fun_cod': funcionario.FUN_COD,
            'nome': funcionario.PES_COD.PES_NOME,
            'email': funcionario.PES_COD.PES_EMAIL,  
            'cargo': funcionario.FUN_ROLES.CARGO_NOME,
            'cargo_cod': funcionario.FUN_ROLES.CARGO_COD,
            'admin': funcionario.FUN_TIPO,
            'vlr_hora': funcionario.FUN_VALOR_HORA,
            'vlr_maximo': funcionario.FUN_MAXIMO_HORAS,
            'cargos': list(cargos)
        }

        return JsonResponse(response_data, safe=False)
    else:
        return JsonResponse({'mensagem': 'Funcionário não encontrado'}, status=404)
    
    
@login_required(login_url='/auth/login/')
def editar_funcionario(request):

        admin = request.POST.get('admin_checkbox');
        cargo_id = request.POST.get('cargo')
        valor_hora = request.POST.get('vlr_hora')
        valor_maximo_horas = request.POST.get('vlr_maximo')
        fun_cod = request.POST.get('fun_cod')
        funcionario = Funcionario.objects.get(FUN_COD=fun_cod)

        if not admin:
            admin = 'F'
        else:
            admin = 'A'
             
        print(request.POST)
        
        cargo_instancia = Cargo.objects.filter(CARGO_COD = cargo_id).first()
        
        funcionario.FUN_TIPO = admin
        funcionario.FUN_ROLES = cargo_instancia 
        funcionario.FUN_VALOR_HORA = valor_hora
        funcionario.FUN_MAXIMO_HORAS = valor_maximo_horas
        funcionario.save()
        return redirect('/plataforma/equipe/')  


@login_required(login_url='/auth/login/')
def aprovar_hora(request):
    if request.method == 'POST':
        try:
            tarefa_codigo = request.POST.get('tarefa_id')
            id = request.POST.get('hora_id')
            
            hr_trablhada = Horas_Trabalhadas.objects.filter(HRT_COD = id).first()


            hr_trablhada.HRF_STATUS = 'AR' 
            hr_trablhada.save()
            tarefa = Tarefas.objects.filter(TRF_COD = tarefa_codigo).first()

            hoje = datetime.datetime.now()
            Horas_Aprovadas(TRF_COD=tarefa, HRA_DT_ULTIMA=hoje)

            return JsonResponse({'message': 'Hora aprovada com sucesso!'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        
        
        
@login_required(login_url='/auth/login/')
def reprovar_hora(request):
    if request.method == 'POST':
        try:
            tarefa_codigo = request.POST.get('tarefa_id')
            id = request.POST.get('hora_id')
            print('id -> ', id)
            hr_trablhada = Horas_Trabalhadas.objects.filter(HRT_COD = id).first()
            
            if not hr_trablhada:
                return JsonResponse({'error': 'horas é necessária'}, status=400)

            
            
            hr_trablhada.HRF_STATUS = 'R' 
            hr_trablhada.save()
            print(tarefa_codigo)
            tarefa = Tarefas.objects.filter(TRF_COD = tarefa_codigo).first()
            
            justificativa = request.POST.get('justificativa')
            if not justificativa:
                return JsonResponse({'error': 'Justificativa é necessária'}, status=400)
            hoje = datetime.datetime.now()
            horas_reprovadas = Horas_Reprovadas(TRF_COD=tarefa, HRR_DT_ULTIMA=hoje, HRR_JUSTIFICATIVA=justificativa)
            horas_reprovadas.save()
            return JsonResponse({'message': 'Justificativa enviada com sucesso!'}, status=200)
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=400)
        
        
@login_required(login_url='/auth/login/')
def invoices(request):
    return render(request, 'invoice.html')


def criar_invoice(request):
    if request.method == 'POST':
        cliente_id = request.POST['cliente']
        funcionario_id = request.POST['funcionario']
        data_inicio = request.POST['dataInicio']
        data_fim = request.POST['dataFim']

        horas = Horas_Aprovadas.objects.filter(
            funcionario_id=funcionario_id,
            data__range=[data_inicio, data_fim]
        )

        total_horas = sum(h.horas for h in horas)
        valor_hora = Funcionario.objects.get(id=funcionario_id).valor_hora
        total_valor = total_horas * valor_hora

        invoice = Invoice.objects.create(
            CLI_COD=cliente_id,
            funcionario_id=funcionario_id,
            total_horas=total_horas,
            total_valor=total_valor
        )
        return JsonResponse({'status': 'success', 'invoice_id': invoice.id})
    return render(request, 'criar_invoice.html')



def gerar_relatorio_invoices(caminho='relatorio_invoices.pdf'):
    pdf = canvas.Canvas(caminho, pagesize=A4)
    largura, altura = A4
    y = altura - 50

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, y, "Relatório de Invoices")
    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, y - 20, f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    y -= 50

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "ID")
    pdf.drawString(100, y, "Cliente")
    pdf.drawString(200, y, "Funcionário")
    pdf.drawString(300, y, "Data Emissão")
    pdf.drawString(400, y, "Total Horas")
    pdf.drawString(500, y, "Total Valor")
    y -= 20
    pdf.line(50, y + 10, largura - 50, y + 10)
    y -= 10

    pdf.setFont("Helvetica", 10)
    invoices = Invoice.objects.all().select_related('CLIENTE', 'FUNCIONARIO') 
    for invoice in invoices:
        if y < 100:  
            pdf.showPage()
            pdf.setFont("Helvetica", 10)
            y = altura - 50

        pdf.drawString(50, y, str(invoice.INV_ID))
        pdf.drawString(100, y, invoice.CLIENTE.nome if invoice.CLIENTE else "N/A")
        pdf.drawString(200, y, invoice.FUNCIONARIO.nome if invoice.FUNCIONARIO else "N/A")
        pdf.drawString(300, y, invoice.DATA_EMISSAO.strftime('%d/%m/%Y'))
        pdf.drawString(400, y, f"{invoice.TOTAL_HORAS:.2f}")
        pdf.drawString(500, y, f"R$ {invoice.TOTAL_VALOR:.2f}")
        y -= 20

    total_valor = invoices.aggregate(Sum('TOTAL_VALOR'))['TOTAL_VALOR__sum'] or 0
    pdf.line(50, y, largura - 50, y)
    y -= 20
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, f"Total Geral: R$ {total_valor:.2f}")

    pdf.save()

    print(f"Relatório gerado com sucesso em {caminho}")