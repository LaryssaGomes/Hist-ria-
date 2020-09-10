# Generated by Django 2.2.11 on 2020-08-24 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuariocomum',
            name='validar_email',
        ),
        migrations.AddField(
            model_name='usuariocomum',
            name='codigo',
            field=models.CharField(default=1, max_length=12, verbose_name='codigo'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='usuariocomum',
            name='cpf',
            field=models.CharField(max_length=15, unique=True, verbose_name='CPF'),
        ),
        migrations.AlterField(
            model_name='usuariocomum',
            name='lattes',
            field=models.FileField(upload_to='documents/%Y/%m/%d', verbose_name='Curriculo lattes'),
        ),
        migrations.AlterField(
            model_name='usuariocomum',
            name='rg',
            field=models.CharField(max_length=13, verbose_name='RG'),
        ),
    ]
