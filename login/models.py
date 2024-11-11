from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,BaseUserManager


class PessoaManager(BaseUserManager):
    def create_user(self, PES_EMAIL, PES_NOME, PES_SOBRENOME, password=None, **extra_fields):
        if not PES_EMAIL:
            raise ValueError('O e-mail é obrigatório')
        PES_EMAIL = self.normalize_email(PES_EMAIL)
        user = self.model(PES_EMAIL=PES_EMAIL, PES_NOME=PES_NOME, PES_SOBRENOME=PES_SOBRENOME, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, PES_EMAIL, PES_NOME, PES_SOBRENOME, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(PES_EMAIL, PES_NOME, PES_SOBRENOME, password, **extra_fields)
class Pessoa(AbstractBaseUser, PermissionsMixin):
    PES_COD = models.AutoField(primary_key=True)
    PES_NOME = models.CharField(max_length=30, null=False)
    PES_SOBRENOME = models.CharField(max_length=20, null=False)
    PES_EMAIL = models.EmailField(max_length=50, null=False, unique=True)  
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    password = models.CharField(max_length=100, null=False) 

    USERNAME_FIELD = 'PES_EMAIL'
    REQUIRED_FIELDS = ['PES_NOME', 'PES_SOBRENOME'] 
    objects = PessoaManager()


    
    class Meta:
        db_table = 'Pessoa' 

class Empresa(models.Model):
    EMP_COD = models.AutoField(primary_key=True)
    EMP_NOME = models.CharField(max_length=50, null=False)
    EMP_NOVO = models.CharField(max_length=1, null=False, default='S')
    PES_COD = models.ForeignKey(Pessoa, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.EMP_NOME} - {self.PES_COD}"  # Correção: você deve referenciar PES_COD, não EMP_EMAIL

    class Meta:
        db_table = 'Empresa' 
