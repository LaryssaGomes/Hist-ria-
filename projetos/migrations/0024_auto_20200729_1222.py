# Generated by Django 2.2.4 on 2020-07-29 15:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projetos', '0023_auto_20200729_1145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arquivo',
            name='arq_tdd_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='projetos.TiposDeDocumento'),
        ),
    ]