from django.db import models
from login.models import Empresa, Pessoa
from datetime import datetime

class EmpresaInfo(models.Model):
      EMI_COD = models.AutoField(primary_key=True)
      EMP_QUANTIDADE_FUNC = models.IntegerField()
      EMP_OBJETIVO =  models.CharField(max_length=100,  blank=True, null=True)
      EMP_COD = models.ForeignKey(Empresa,  on_delete=models.CASCADE)
      DATA_CRIACAO = models.DateTimeField(auto_now_add=True) 

      
class Cargo(models.Model):
    CARGO_COD = models.AutoField(primary_key=True)
    CARGO_NOME  = models.CharField(max_length=60, unique=True)
    CARGO_DT_ATUALIZACAO = models.DateTimeField(default=datetime.now)
    
class Funcionario(models.Model): 
    FUN_COD  = models.AutoField(primary_key=True)
    PES_COD  = models.ForeignKey(Pessoa, on_delete=models.CASCADE)
    EMP_COD  = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    FUNC_DT_CADASTRO = models.DateTimeField(default=datetime.now)
    FUN_ROLES = models.ForeignKey(Cargo, on_delete=models.DO_NOTHING)
    FUN_MAXIMO_HORAS = models.IntegerField()
    FUN_VALOR_HORA = models.DecimalField(max_digits=10, decimal_places=2)  # Defina valores
  
class Cliente(models.Model):
    CLI_COD  = models.AutoField(primary_key=True)
    CLI_NOME = models.CharField(max_length=50,  blank=False, null=False)
    CLI_RAMO_ATUACAO  = models.CharField(max_length=50,  blank=True, null=True)
    CLI_CNPJ = models.CharField(max_length=18,  blank=True, null=True, unique=True)
    EMP_COD  = models.ForeignKey(Empresa, on_delete=models.CASCADE)


class Projeto(models.Model):
     PJT_COD = models.AutoField(primary_key=True)
     PJT_NOME = models.CharField(max_length= 150)
     CLI_COD = models.ForeignKey(Cliente, on_delete=models.CASCADE)


class Prioridade(models.Model):
     PRI_COD = models.AutoField(primary_key=True)
     PRI_NOME = models.CharField(max_length= 50)
     
class Tarefas(models.Model):
    TRF_COD = models.AutoField(primary_key=True)
    PJT_COD = models.ForeignKey(Projeto, on_delete=models.CASCADE)
    TRF_TITULO = models.CharField(max_length=200, blank=False, null=False)
    PES_COD = models.ForeignKey(Pessoa, on_delete=models.CASCADE)
    TRF_PRIORIDADE = models.ForeignKey(Prioridade, on_delete=models.CASCADE)
    TRF_STATUS = models.CharField(max_length=10, choices=[('P', 'Pendente'), ('C', 'Concluída'), ('A', 'Atrasada')])
    TRF_DATA_PRAZO = models.DateField()
    
class CategoriaHoras(models.Model):
   CTH_COD = models.AutoField(primary_key=True)
   CTH_NOME = models.CharField(max_length=100, blank=False, null=False)
    
class Horas(models.Model):
    HRO_COD = models.AutoField(primary_key=True)
    HRO_OBSERVACAO = models.CharField(max_length=150)
    HRO_CATEGORIA = models.ForeignKey(CategoriaHoras, on_delete=models.CASCADE)
    
