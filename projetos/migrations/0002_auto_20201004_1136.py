# Generated by Django 3.1.1 on 2020-10-04 14:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0002_auto_20201004_1136'),
        ('projetos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='arquivo',
            name='arq_pro_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='projetos.projetos'),
        ),
        migrations.AddField(
            model_name='arquivo',
            name='arq_tdd_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='projetos.tiposdedocumento'),
        ),
        migrations.AddField(
            model_name='audio',
            name='aud_arq',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='audio', to='projetos.arquivo'),
        ),
        migrations.AddField(
            model_name='documento',
            name='doc_arq',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='projetos.arquivo'),
        ),
        migrations.AddField(
            model_name='fotos',
            name='fot_arq',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='projetos.arquivo'),
        ),
        migrations.AddField(
            model_name='notificacao',
            name='noti_arquivo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='projetos.projetos'),
        ),
        migrations.AddField(
            model_name='notificacao',
            name='noti_bolsista',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bolsista', to='usuario.usuariocomum'),
        ),
        migrations.AddField(
            model_name='notificacao',
            name='noti_pesquisador',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pesquisador', to='usuario.usuariocomum'),
        ),
        migrations.AddField(
            model_name='patrimoniocultura',
            name='pc_arq',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='patrimoniocultura', to='projetos.arquivo'),
        ),
        migrations.AddField(
            model_name='projetos',
            name='pro_inst',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='projetos.instituicao'),
        ),
        migrations.AddField(
            model_name='projetos',
            name='pro_usuarios',
            field=models.ManyToManyField(through='projetos.ProjetosDosUsuarios', to='usuario.UsuarioComum'),
        ),
        migrations.AddField(
            model_name='projetosdosusuarios',
            name='pdu_usuarios',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='usuario.usuariocomum'),
        ),
    ]
