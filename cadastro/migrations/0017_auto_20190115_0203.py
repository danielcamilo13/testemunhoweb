# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-01-15 04:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastro', '0016_auto_20190102_2158'),
    ]

    operations = [
        migrations.AddField(
            model_name='irmaos',
            name='conjuge',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='dias',
            name='max',
            field=models.CharField(max_length=3, null=True, verbose_name='Qte max no mes'),
        ),
    ]
