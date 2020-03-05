# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models

class consulta(models.Model):
    id = models.AutoField(primary_key=True)
    mes = models.CharField(max_length=25,null=True,verbose_name='mes',blank=True)
