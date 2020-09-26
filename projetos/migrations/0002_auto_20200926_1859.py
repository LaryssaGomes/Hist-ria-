# Generated by Django 2.2.4 on 2020-09-26 21:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usuario', '0001_initial'),
        ('projetos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='projetosdosusuarios',
            name='pdu_usuarios',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='usuario.UsuarioComum'),
        ),
        migrations.AddField(
            model_name='projetos',
            name='pro_inst',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='projetos.Instituicao'),
        ),
        migrations.AddField(
            model_name='projetos',
            name='pro_usuarios',
            field=models.ManyToManyField(through='projetos.ProjetosDosUsuarios', to='usuario.UsuarioComum'),
        ),
        migrations.AddField(
            model_name='patrimoniocultura',
            name='pc_arq',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='patrimoniocultura', to='projetos.Arquivo'),
        ),
        migrations.AddField(
            model_name='notificacao',
            name='noti_arquivo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='projetos.Projetos'),
        ),
        migrations.AddField(
            model_name='notificacao',
            name='noti_bolsista',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bolsista', to='usuario.UsuarioComum'),
        ),
        migrations.AddField(
            model_name='notificacao',
            name='noti_pesquisador',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pesquisador', to='usuario.UsuarioComum'),
        ),
        migrations.AddField(
            model_name='fotos',
            name='fot_arq',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='projetos.Arquivo'),
        ),
        migrations.AddField(
            model_name='documento',
            name='doc_arq',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='projetos.Arquivo'),
        ),
        migrations.AddField(
            model_name='audio',
            name='aud_arq',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='audio', to='projetos.Arquivo'),
        ),
        migrations.AddField(
            model_name='arquivo',
            name='arq_pro_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='projetos.Projetos'),
        ),
        migrations.AddField(
            model_name='arquivo',
            name='arq_tdd_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='projetos.TiposDeDocumento'),
        ),
    ]
