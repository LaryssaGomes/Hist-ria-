# Generated by Django 2.2.4 on 2020-07-21 00:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projetos', '0012_auto_20200720_1216'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='arquivo',
            name='arq_palavras_chaves',
        ),
        migrations.CreateModel(
            name='PalavrasChave',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pc_palavras_chaves', models.CharField(max_length=200, null=True, verbose_name='Palavras chaves:')),
                ('pc_arq', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='projetos.Arquivo')),
            ],
        ),
    ]
