# Generated by Django 4.2.7 on 2024-04-09 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menuinicial', '0005_alter_funcionario_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funcionario',
            name='password',
            field=models.CharField(default='pbkdf2_sha256$600000$b9Z4VLMfdI5eTbWbkG9BWD$+1puCSvspMV/Xf94iVmsYqhbLyRIkjGFWNL/d0TGV4M=', max_length=128),
        ),
    ]
