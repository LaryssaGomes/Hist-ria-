# Generated by Django 2.2.4 on 2020-08-15 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetos', '0033_auto_20200814_2306'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='arquivo',
            name='arq_tutilo',
        ),
        migrations.AddField(
            model_name='arquivo',
            name='arq_nome',
            field=models.CharField(max_length=100, null=True, verbose_name='Nome:'),
        ),
    ]