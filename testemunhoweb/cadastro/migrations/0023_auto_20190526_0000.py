# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-05-26 03:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastro', '0022_irmaoslista'),
    ]

    operations = [
        migrations.AlterField(
            model_name='irmaos',
            name='estado_civil',
            field=models.CharField(choices=[('solteiro', 'solteiro'), ('casado', 'casado'), ('viuvo', 'viuvo')], max_length=30, null=True, verbose_name='Estado Civil'),
        ),
    ]