# Generated by Django 3.2.10 on 2021-12-31 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contatos', '0002_contato_mostrar'),
    ]

    operations = [
        migrations.AddField(
            model_name='contato',
            name='foto',
            field=models.ImageField(blank=True, upload_to='pictures/%Y/%m/%d'),
        ),
    ]
