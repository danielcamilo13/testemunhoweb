# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2018-12-28 02:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastro', '0011_auto_20181226_0321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dias',
            name='max',
            field=models.CharField(default=0, max_length=3, verbose_name='Qte de vezes no mes'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dias',
            name='p1',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='dias',
            name='p1_1',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='dias',
            name='p1_2',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='dias',
            name='p2',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='dias',
            name='p2_1',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='dias',
            name='p3',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='dias',
            name='p3_1',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='dias',
            name='p4',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='dias',
            name='p4_1',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='dias',
            name='p5',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='dias',
            name='p5_1',
            field=models.BooleanField(default=False),
        ),
    ]
