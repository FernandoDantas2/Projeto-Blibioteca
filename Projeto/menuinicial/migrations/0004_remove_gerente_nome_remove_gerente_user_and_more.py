# Generated by Django 4.2.7 on 2024-04-09 02:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menuinicial', '0003_alter_funcionario_password_alter_gerente_cpf'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gerente',
            name='nome',
        ),
        migrations.RemoveField(
            model_name='gerente',
            name='user',
        ),
        migrations.RemoveField(
            model_name='solicitacaocadastro',
            name='aprovado',
        ),
        migrations.AddField(
            model_name='gerente',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
        migrations.AddField(
            model_name='gerente',
            name='password',
            field=models.CharField(default=2, max_length=128, verbose_name='password'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='funcionario',
            name='password',
            field=models.CharField(default='pbkdf2_sha256$600000$GjIjvJVtWQhjB3GTHFG77x$nOYRDOuc56H9GPIkqjT9OXwoIvEBpJr2eaUNrGO0zxo=', max_length=128),
        ),
        migrations.AlterField(
            model_name='solicitacaocadastro',
            name='funcionario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]