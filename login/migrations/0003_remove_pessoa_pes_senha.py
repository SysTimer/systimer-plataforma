# Generated by Django 5.1 on 2024-11-10 22:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_pessoa_is_active_pessoa_is_staff_pessoa_last_login_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pessoa',
            name='PES_SENHA',
        ),
    ]