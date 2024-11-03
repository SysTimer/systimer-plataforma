from tkinter import CASCADE
from django.db import models



class Pessoa(models.Model):
    PES_COD = models.AutoField(primary_key=True)
    PES_NOME = models.CharField(max_length=30, null=False)
    PES_SOBRENOME = models.CharField(max_length=20, null=False)
    PES_SENHA = models.CharField(max_length=100, null=False)
    PES_EMAIL = models.EmailField(max_length=50, null=False, unique=True)  

    

class Empresa(models.Model):
    EMP_COD = models.AutoField(primary_key=True)
    EMP_NOME = models.CharField(max_length=50, null=False)
    EMP_NOVO =  models.CharField(max_length=1, null=False,  default='N')
    PES_COD = models.ForeignKey(Pessoa, on_delete= models.CASCADE)
    
    def __str__(self):
        return f"{self.EMP_NOME} - {self.EMP_EMAIL}"