# Generated by Django 5.1.2 on 2024-11-03 19:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pessoa',
            fields=[
                ('PES_COD', models.AutoField(primary_key=True, serialize=False)),
                ('PES_NOME', models.CharField(max_length=30)),
                ('PES_SOBRENOME', models.CharField(max_length=20)),
                ('PES_SENHA', models.CharField(max_length=100)),
                ('PES_EMAIL', models.EmailField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('EMP_COD', models.AutoField(primary_key=True, serialize=False)),
                ('EMP_NOME', models.CharField(max_length=50)),
                ('EMP_NOVO', models.CharField(default='N', max_length=1)),
                ('PES_COD', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.pessoa')),
            ],
        ),
    ]
