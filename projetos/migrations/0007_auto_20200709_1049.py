# Generated by Django 3.0.6 on 2020-07-09 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetos', '0006_auto_20200706_0948'),
    ]

    operations = [
        migrations.AddField(
            model_name='arquivo',
            name='arq_destinatario',
            field=models.CharField(max_length=200, null=True, verbose_name='Destinatario:'),
        ),
        migrations.AddField(
            model_name='arquivo',
            name='arq_emitente',
            field=models.CharField(max_length=200, null=True, verbose_name='Emitente:'),
        ),
    ]
