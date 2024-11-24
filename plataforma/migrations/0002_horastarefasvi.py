# Generated by Django 5.1 on 2024-11-23 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plataforma', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HorasTarefasVI',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trf_cod', models.IntegerField()),
                ('pes_cod', models.IntegerField()),
                ('emp_cod_id', models.IntegerField()),
                ('trf_titulo', models.CharField(max_length=200)),
                ('pjt_nome', models.CharField(max_length=150)),
                ('pri_nome', models.CharField(max_length=50)),
                ('total_tempo_trabalhado', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'SYS_TAREFAS_VI',
                'managed': False,
            },
        ),
    ]
