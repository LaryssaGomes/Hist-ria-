# Generated by Django 2.2.4 on 2020-08-16 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projetos', '0043_auto_20200816_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patrimoniocultura',
            name='pc_lugares',
            field=models.TextField(blank=True, max_length=100, null=True, verbose_name='Lugares:'),
        ),
    ]