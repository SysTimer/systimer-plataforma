# Generated by Django 5.1 on 2024-11-30 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plataforma', '0010_cargo_emp_cod'),
    ]

    operations = [
        migrations.CreateModel(
            name='SysEquipeVi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pes_nome', models.CharField(max_length=255)),
                ('pes_email', models.EmailField(max_length=254)),
                ('cargo_nome', models.CharField(max_length=255)),
                ('trabalho', models.BooleanField()),
                ('pes_foto_url', models.URLField(blank=True, max_length=500, null=True)),
                ('pes_cod', models.BigIntegerField()),
                ('fun_cod', models.BigIntegerField()),
                ('emp_cod_id', models.BigIntegerField()),
            ],
            options={
                'db_table': 'SYS_EQUIPE_VI',
                'managed': False,
            },
        ),
    ]