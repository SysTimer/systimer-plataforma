# Generated by Django 5.1 on 2024-11-24 20:37

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('login', '0009_loginauditoria'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EmpresaPessoaView',
            fields=[
                ('pes_cod', models.IntegerField(primary_key=True, serialize=False)),
                ('pes_nome', models.CharField(max_length=150)),
                ('emp_nome', models.CharField(max_length=150)),
                ('emp_cod', models.IntegerField()),
                ('cargo_nome', models.CharField(max_length=150)),
                ('Dono', models.IntegerField()),
                ('UltimoAcesso', models.CharField(max_length=150)),
            ],
            options={
                'db_table': 'EMPRESA_PESSOA_VI',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='HorasTarefasVI',
            fields=[
                ('trf_cod', models.IntegerField(primary_key=True, serialize=False)),
                ('pes_cod', models.IntegerField()),
                ('emp_cod_id', models.IntegerField()),
                ('trf_titulo', models.CharField(max_length=200)),
                ('pjt_nome', models.CharField(max_length=150)),
                ('pri_nome', models.CharField(max_length=50)),
                ('CLI_NOME', models.CharField(max_length=150)),
                ('total_tempo_trabalhado', models.CharField(max_length=40)),
                ('dt_inicio_iniciada', models.CharField(max_length=40)),
                ('status_tarefa', models.CharField(max_length=40)),
            ],
            options={
                'db_table': 'SYS_TAREFAS_VI',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('CARGO_COD', models.AutoField(primary_key=True, serialize=False)),
                ('CARGO_NOME', models.CharField(max_length=60, unique=True)),
                ('CARGO_DT_ATUALIZACAO', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'Cargo',
            },
        ),
        migrations.CreateModel(
            name='Prioridade',
            fields=[
                ('PRI_COD', models.AutoField(primary_key=True, serialize=False)),
                ('PRI_NOME', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'Prioridade',
            },
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('CLI_COD', models.AutoField(primary_key=True, serialize=False)),
                ('CLI_NOME', models.CharField(max_length=50)),
                ('CLI_RAMO_ATUACAO', models.CharField(blank=True, max_length=50, null=True)),
                ('CLI_CNPJ', models.CharField(blank=True, max_length=18, null=True, unique=True)),
                ('EMP_COD', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.empresa')),
            ],
            options={
                'db_table': 'Cliente',
            },
        ),
        migrations.CreateModel(
            name='EmpresaInfo',
            fields=[
                ('EMI_COD', models.AutoField(primary_key=True, serialize=False)),
                ('EMP_QUANTIDADE_FUNC', models.IntegerField()),
                ('EMP_OBJETIVO', models.CharField(blank=True, max_length=100, null=True)),
                ('DATA_CRIACAO', models.DateTimeField(auto_now_add=True)),
                ('EMP_COD', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.empresa')),
            ],
            options={
                'db_table': 'EmpresaInfo',
            },
        ),
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('FUN_COD', models.AutoField(primary_key=True, serialize=False)),
                ('FUNC_DT_CADASTRO', models.DateTimeField(default=django.utils.timezone.now)),
                ('FUN_MAXIMO_HORAS', models.IntegerField()),
                ('FUN_VALOR_HORA', models.DecimalField(decimal_places=2, max_digits=10)),
                ('EMP_COD', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.empresa')),
                ('FUN_ROLES', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='plataforma.cargo')),
                ('PES_COD', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Funcionario',
            },
        ),
        migrations.CreateModel(
            name='Horas_Trabalhadas',
            fields=[
                ('HRT_COD', models.AutoField(primary_key=True, serialize=False)),
                ('HRT_DT_INICIO', models.DateTimeField(default=django.utils.timezone.now)),
                ('HRT_DT_FIM', models.DateTimeField(blank=True, null=True)),
                ('HRF_STATUS', models.CharField(default='A', max_length=1)),
                ('PES_COD', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Horas_Trabalhadas',
            },
        ),
        migrations.CreateModel(
            name='Horas_Reprovadas',
            fields=[
                ('HRR_COD', models.AutoField(primary_key=True, serialize=False)),
                ('HRR_DT_ULTIMA', models.DateTimeField(default=django.utils.timezone.now)),
                ('HRR_JUSTIFICATIVA', models.CharField(max_length=200)),
                ('HRT_COD', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataforma.horas_trabalhadas')),
            ],
            options={
                'db_table': 'Horas_Reprovadas',
            },
        ),
        migrations.CreateModel(
            name='Projeto',
            fields=[
                ('PJT_COD', models.AutoField(primary_key=True, serialize=False)),
                ('PJT_NOME', models.CharField(max_length=150)),
                ('CLI_COD', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataforma.cliente')),
            ],
            options={
                'db_table': 'Projeto',
            },
        ),
        migrations.CreateModel(
            name='Tarefas',
            fields=[
                ('TRF_COD', models.AutoField(primary_key=True, serialize=False)),
                ('TRF_TITULO', models.CharField(max_length=200)),
                ('TRF_DATA_PRAZO', models.DateField()),
                ('TRF_STATUS', models.CharField(default='A', max_length=1)),
                ('PES_COD', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('PJT_COD', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataforma.projeto')),
                ('TRF_PRIORIDADE', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataforma.prioridade')),
            ],
            options={
                'db_table': 'Tarefas',
            },
        ),
        migrations.AddField(
            model_name='horas_trabalhadas',
            name='TRF_COD',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataforma.tarefas'),
        ),
    ]
