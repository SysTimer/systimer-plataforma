# Generated by Django 5.1 on 2024-12-01 21:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plataforma', '0017_horas_aprovadas'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='horas_aprovadas',
            name='HRA_JUSTIFICATIVA',
        ),
    ]
