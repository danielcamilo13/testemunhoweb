# Generated by Django 2.2.7 on 2019-12-13 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastro', '0041_auto_20191213_0003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='designacao',
            name='dia_mes',
            field=models.IntegerField(verbose_name='Dia Mes'),
        ),
    ]
