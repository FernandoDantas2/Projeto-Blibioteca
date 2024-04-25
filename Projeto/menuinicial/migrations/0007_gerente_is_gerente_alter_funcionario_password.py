# Generated by Django 4.2.7 on 2024-04-09 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menuinicial', '0006_alter_funcionario_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='gerente',
            name='is_gerente',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='funcionario',
            name='password',
            field=models.CharField(default='pbkdf2_sha256$600000$6iIZ6335W9DFJTC6nSskYc$gvqT66E2oXLdzZ6auVurT8DUVBcupDDNRpF29vFpQLY=', max_length=128),
        ),
    ]