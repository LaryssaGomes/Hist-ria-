# Generated by Django 2.2.4 on 2020-07-29 14:45

from django.db import migrations, models
import projetos.models


class Migration(migrations.Migration):

    dependencies = [
        ('projetos', '0022_auto_20200729_1136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audio',
            name='aud_audio',
            field=models.FileField(blank=True, null=True, upload_to=projetos.models.user_directory_path_audio_file, verbose_name='Audio'),
        ),
        migrations.AlterField(
            model_name='documento',
            name='doc_documento',
            field=models.FileField(blank=True, null=True, upload_to=projetos.models.user_directory_path_documento_file, verbose_name='Documento'),
        ),
        migrations.AlterField(
            model_name='video',
            name='vid_video',
            field=models.FileField(blank=True, null=True, upload_to=projetos.models.user_directory_path_video_file, verbose_name='Video:'),
        ),
    ]
