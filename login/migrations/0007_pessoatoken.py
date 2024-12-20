# Generated by Django 5.1 on 2024-11-11 00:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0006_pessoa_groups_pessoa_is_superuser_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PessoaToken',
            fields=[
                ('PST_COD', models.AutoField(primary_key=True, serialize=False)),
                ('PST_TOKEN', models.CharField(max_length=80, unique=True)),
                ('PST_DATA_EXPIRACAO', models.DateField()),
                ('PST_EXPIRADO', models.CharField(default='N', max_length=1)),
                ('PES_COD', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Pessoa_Token',
            },
        ),
    ]
