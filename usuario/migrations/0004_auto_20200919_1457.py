# Generated by Django 2.2.16 on 2020-09-19 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0003_auto_20200919_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuariocomum',
            name='lattes',
            field=models.URLField(verbose_name='Curriculo'),
        ),
    ]
