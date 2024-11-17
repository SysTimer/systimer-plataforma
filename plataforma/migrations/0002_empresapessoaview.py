# Generated by Django 5.1 on 2024-11-16 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plataforma', '0001_initial'),
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
    ]
