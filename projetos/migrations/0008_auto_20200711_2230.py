# Generated by Django 3.0.6 on 2020-07-12 01:30

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projetos', '0007_auto_20200709_1049'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='audio',
            name='aud_texto',
        ),
        migrations.RemoveField(
            model_name='documento',
            name='doc_texto',
        ),
        migrations.RemoveField(
            model_name='video',
            name='vid_texto',
        ),
        migrations.AddField(
            model_name='arquivo',
            name='arq_texto',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, max_length=1000, null=True),
        ),
        migrations.DeleteModel(
            name='Transcricao',
        ),
    ]
