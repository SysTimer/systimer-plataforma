# Generated by Django 5.1 on 2024-12-02 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0013_alter_pessoa_pes_foto_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pessoa',
            name='PES_FOTO_REFERENCIA',
            field=models.ImageField(blank=True, null=True, upload_to='fotos_perfil/'),
        ),
    ]
