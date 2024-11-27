from django.db import models
from django.utils import timezone
from login.models import Empresa, Pessoa

class EmpresaInfo(models.Model):
    EMI_COD = models.AutoField(primary_key=True)
    EMP_QUANTIDADE_FUNC = models.IntegerField()
    EMP_RAMO_ATUACAO = models.CharField(max_length=100, blank=True, null=True)
    EMP_COD = models.ForeignKey(Empresa, unique=True, on_delete=models.CASCADE)
    DATA_CRIACAO = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'EmpresaInfo' 

class Cargo(models.Model):
    CARGO_COD = models.AutoField(primary_key=True)
    CARGO_NOME = models.CharField(max_length=60, unique=True)
    CARGO_DT_ATUALIZACAO = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'Cargo' 

class Funcionario(models.Model):
    FUN_COD = models.AutoField(primary_key=True)
    PES_COD = models.ForeignKey(Pessoa, on_delete=models.CASCADE)
    EMP_COD = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    FUNC_DT_CADASTRO = models.DateTimeField(default=timezone.now)
    FUN_ROLES = models.ForeignKey(Cargo, on_delete=models.DO_NOTHING)
    FUN_MAXIMO_HORAS = models.IntegerField(blank=True, null=True)
    FUN_VALOR_HORA = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'Funcionario' 

class Cliente(models.Model):
    CLI_COD = models.AutoField(primary_key=True)
    CLI_NOME = models.CharField(max_length=50, blank=False, null=False)
    EMP_COD = models.ForeignKey(Empresa, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Cliente' 

class Projeto(models.Model):
    PJT_COD = models.AutoField(primary_key=True)
    PJT_NOME = models.CharField(max_length=150)
    CLI_COD = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Projeto' 

class Prioridade(models.Model):
    PRI_COD = models.AutoField(primary_key=True)
    PRI_NOME = models.CharField(max_length=50)

    class Meta:
        db_table = 'Prioridade' 

class Tarefas(models.Model):
    TRF_COD = models.AutoField(primary_key=True)
    PJT_COD = models.ForeignKey(Projeto, on_delete=models.CASCADE)
    TRF_TITULO = models.CharField(max_length=200, blank=False, null=False)
    FUN_COD = models.ForeignKey(Funcionario, on_delete=models.CASCADE)  # Mudou aqui
    TRF_PRIORIDADE = models.ForeignKey(Prioridade, on_delete=models.CASCADE)
    TRF_DATA_CONCLUSAO = models.DateTimeField(blank=True, null=True)
    TRF_STATUS = models.CharField(max_length=2, default='A')
    TRF_DATA_CRIACAO =  models.DateTimeField(auto_now=True)
    TRF_OBSERVACAO =  models.CharField(max_length=120, blank=True)
    class Meta:
        db_table = 'Tarefas' 


class Horas_Trabalhadas(models.Model):
    HRT_COD = models.AutoField(primary_key=True)
    HRT_DT_INICIO = models.DateTimeField(default=timezone.now)
    HRT_DT_FIM = models.DateTimeField(blank=True, null=True)
    PES_COD = models.ForeignKey(Pessoa, on_delete=models.CASCADE)
    TRF_COD = models.ForeignKey(Tarefas, on_delete=models.CASCADE)
    HRF_STATUS = models.CharField(max_length=2, default='A')
    class Meta:
        db_table = 'Horas_Trabalhadas' 


class Horas_Reprovadas(models.Model):
    HRR_COD = models.AutoField(primary_key=True)
    HRR_DT_ULTIMA = models.DateTimeField(default=timezone.now)
    HRR_JUSTIFICATIVA = models.CharField(max_length=200, blank=False, null=False)
    TRF_COD = models.ForeignKey(Tarefas, on_delete=models.CASCADE)
    class Meta:
        db_table = 'Horas_Reprovadas' 

class EmpresaPessoaView(models.Model):
    pes_cod = models.IntegerField(primary_key=True) 
    pes_nome = models.CharField(max_length=150)
    emp_nome = models.CharField(max_length=150)
    emp_cod = models.IntegerField() 
    cargo_nome = models.CharField(max_length=150)
    Dono = models.IntegerField() 
    UltimoAcesso = models.CharField(max_length=150)

    class Meta():
        db_table = "SYS_LISTAR_EMPRESA_VI"
        managed = False
        
    
class HorasTarefasVI(models.Model):
    trf_cod = models.IntegerField(primary_key=True)
    fun_cod = models.IntegerField()
    emp_cod_id = models.IntegerField()
    trf_titulo = models.CharField(max_length=200)  
    pjt_nome = models.CharField(max_length=150)  
    pri_nome = models.CharField(max_length=50) 
    CLI_NOME = models.CharField(max_length=150)  
    total_tempo_trabalhado = models.CharField(max_length=40) 
    dt_inicio_iniciada = models.CharField(max_length=40) 
    status_tarefa = models.CharField(max_length=40) 
    class Meta:
        db_table = "SYS_TAREFAS_VI" 
        managed = False  
        
        
class SysDetalhesTarefasVi(models.Model):
    trf_cod = models.IntegerField(primary_key=True)
    nome_tarefa = models.CharField(max_length=200)
    nome_cliente = models.CharField(max_length=50)
    prioridade = models.CharField(max_length=50)
    total_horas_trabalhadas = models.CharField(max_length=40) 
    trf_data_conclusao = models.CharField(max_length=10) 
    status = models.CharField(max_length=9)
    trf_data_criacao = models.CharField(max_length=10)  
    trf_status = models.CharField(max_length=10)
    fun_cod = models.IntegerField()  
    pes_cod = models.IntegerField()  
    HRR_JUSTIFICATIVA = models.CharField(max_length=255, null=True, blank=True) 

    class Meta:
        managed = False 
        db_table = 'SYS_DETALHES_TAREFAS_VI'  
        
        
        
class SysGraficosHorasVi(models.Model):
    trf_titulo = models.CharField(max_length=255) 
    data_inicio = models.CharField(max_length=10)
    data_fim = models.CharField(max_length=10) 
    total_trabalhado = models.TimeField() 
    PES_COD_id = models.IntegerField()
    TRF_COD_id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False  # Indica que o Django não gerenciará essa tabela/view
        db_table = 'SYS_GRAFICOS_HORAS_VI'  # Nome da view no banco de dados