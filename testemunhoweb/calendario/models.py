from django.db import models
from datetime import datetime

class calendario(models.Model):
    titulo = models.CharField(verbose_name='Titulo',max_length=55,blank=True,null=True)
    descricao= models.CharField(verbose_name='Descricao',max_length=150,blank=True,null=True)
    data_inicial = models.DateTimeField(verbose_name='Data Inicial',auto_now_add=datetime.now())
    data_final = models.DateTimeField(verbose_name='Data Final',auto_now_add=datetime.now())
    def __str__(self):
        return self.titulo
    def was_published(self):
        return self.data_inicial>=timezone.now() - datetime.timedelta(days=1)