# Generated by Django 5.1 on 2024-12-01 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plataforma', '0013_funcionario_fun_aprovado'),
    ]

    operations = [
        migrations.AddField(
            model_name='funcionario',
            name='FUN_TOKEN',
            field=models.CharField(default=2, max_length=200),
            preserve_default=False,
        ),
    ]
