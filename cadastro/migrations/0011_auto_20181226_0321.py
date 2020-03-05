# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2018-12-26 05:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastro', '0010_auto_20181223_2252'),
    ]

    operations = [
        migrations.AddField(
            model_name='dias',
            name='max',
            field=models.CharField(max_length=3, null=True, verbose_name='Qte de vezes no mes'),
        ),
        migrations.AddField(
            model_name='dias',
            name='p1_1',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dias',
            name='p1_2',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dias',
            name='p2_1',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dias',
            name='p3_1',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dias',
            name='p4_1',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dias',
            name='p5',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dias',
            name='p5_1',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
