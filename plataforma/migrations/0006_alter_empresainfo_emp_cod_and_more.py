# Generated by Django 5.1 on 2024-11-26 23:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0010_pessoa_pes_administrador'),
        ('plataforma', '0005_remove_cliente_cli_cnpj'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empresainfo',
            name='EMP_COD',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.empresa', unique=True),
        ),
        migrations.AlterField(
            model_name='horas_trabalhadas',
            name='HRF_STATUS',
            field=models.CharField(default='A', max_length=2),
        ),
        migrations.AlterField(
            model_name='tarefas',
            name='TRF_STATUS',
            field=models.CharField(default='A', max_length=2),
        ),
    ]