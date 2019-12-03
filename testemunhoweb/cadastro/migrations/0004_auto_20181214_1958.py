# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2018-12-14 21:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cadastro', '0003_auto_20181214_1958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='irmaos',
            name='dia',
            field=models.ForeignKey(default=1, max_length=25, null=True, on_delete=django.db.models.deletion.CASCADE, to='cadastro.dia', verbose_name='Dias Semana'),
        ),
        migrations.AlterField(
            model_name='irmaos',
            name='periodo',
            field=models.ForeignKey(default=1, max_length=30, null=True, on_delete=django.db.models.deletion.CASCADE, to='cadastro.periodo', verbose_name='Periodo'),
        ),
    ]
