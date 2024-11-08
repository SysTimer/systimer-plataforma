from django.db import models
from django.utils import timezone
from login.models import Empresa, Pessoa

class EmpresaInfo(models.Model):
    EMI_COD = models.AutoField(primary_key=True)
    EMP_QUANTIDADE_FUNC = models.IntegerField()
    EMP_OBJETIVO = models.CharField(max_length=100, blank=True, null=True)
    EMP_COD = models.ForeignKey(Empresa, on_delete=models.CASCADE)
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
    FUN_MAXIMO_HORAS = models.IntegerField()
    FUN_VALOR_HORA = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'Funcionario' 

class Cliente(models.Model):
    CLI_COD = models.AutoField(primary_key=True)
    CLI_NOME = models.CharField(max_length=50, blank=False, null=False)
    CLI_RAMO_ATUACAO = models.CharField(max_length=50, blank=True, null=True)
    CLI_CNPJ = models.CharField(max_length=18, blank=True, null=True, unique=True)
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
    PES_COD = models.ForeignKey(Pessoa, on_delete=models.CASCADE)
    TRF_PRIORIDADE = models.ForeignKey(Prioridade, on_delete=models.CASCADE)
    TRF_STATUS = models.CharField(max_length=10, choices=[('P', 'Pendente'), ('C', 'Concluída'), ('A', 'Atrasada')])
    TRF_DATA_PRAZO = models.DateField()

    class Meta:
        db_table = 'Tarefas' 

class CategoriaHoras(models.Model):
    CTH_COD = models.AutoField(primary_key=True)
    CTH_NOME = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        db_table = 'CategoriaHoras' 

class Horas(models.Model):
    HRO_COD = models.AutoField(primary_key=True)
    HRO_OBSERVACAO = models.CharField(max_length=150)
    HRO_CATEGORIA = models.ForeignKey(CategoriaHoras, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Horas' 
