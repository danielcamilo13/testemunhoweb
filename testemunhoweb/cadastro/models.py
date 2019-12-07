# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.utils import timezone

# @python_2_unicode_compatible
class irmaos(models.Model):
    sm = 'Servo Ministerial'
    anc = 'Anciao'
    diant = (
        (sm,'Servo Ministerial'),
        (anc,'Anciao'),
        )
    pr = 'pioneiro regular'
    pa = 'pioneiro auxiliar'
    pu = 'publicador'
    sr = 'servo'
    an = 'anciao'
    priv = (
        (pr,'pioneiro regular'),
        (pa,'pioneiro auxiliar'),
        (pu,'publicador'),
        (sr,'servo ministerial'),
        (an,'anciao'),
    )
    
    sol = 'solteiro'
    cas = 'casado'
    viu = 'viuvo'
    est_civ = (
        (sol,'solteiro'),
        (cas,'casado'),
        (viu,'viuvo'),
    )
    
    mas = 'masculino'
    fem = 'feminino'
    gr_choices = (
        (mas,'masculino'),
        (fem,'feminino'),
    )    
    
    id = models.AutoField(primary_key=True)
    nm = models.CharField(verbose_name='Nome do irmao',blank=False,null=False,max_length=55)
    nm_completo = models.CharField(verbose_name='Nome completo',blank=True,null=True,max_length=120)
    cgcao = models.CharField(verbose_name='Congregação',max_length=90,default='Palmares')
    gr = models.CharField(verbose_name='Gênero',blank=False,max_length=30,choices=gr_choices)
    estado_civil = models.CharField(choices=est_civ,null=True,verbose_name='Estado Civil',max_length=30)
    bairro = models.CharField(max_length=50,verbose_name='Bairro',default='Palmares')
    conjuge = models.CharField(max_length=50,blank=True,null=True)
    habilitado = models.BooleanField(default=True,verbose_name='Habilitado',null=False)
    trio = models.BooleanField(default=False,verbose_name='Trio',null=False)
    excecao_nome = models.CharField(max_length=90,blank=True,null=True,verbose_name='Excecao com nomes')
    excecao_dia = models.CharField(max_length=30,blank=True,null=True,verbose_name='Excecao para dias ')
    grupo = models.CharField(max_length=5,blank=True,null=True,verbose_name='Grupo')
    maximo = models.CharField(max_length=3,verbose_name='max p/m',default=3)
    privilegio = models.CharField(max_length=20,choices=priv,null=True,verbose_name='Privilegio',default='publicador')
    dianteira = models.CharField(max_length=20,choices=diant,null=True,verbose_name='Dianteira',blank=True)
    endereco = models.CharField(max_length=100,null=True,verbose_name='endereco',blank=True)
    telefone1 = models.CharField(max_length=25,null=True,verbose_name='Telefone 1',blank=True)
    telefone2 = models.CharField(max_length=25,null=True,verbose_name='Telefone 2',blank=True)
    nasc = models.DateField(null=True,verbose_name='Data de Nascimento',blank=True)
    batismo = models.DateField(null=True,verbose_name='Data de Batismo',blank=True)
    email = models.EmailField(verbose_name='Email',default='email@email.com')
    dtModificado = models.DateField(verbose_name='Data de modificacao',default=timezone.now)
    obs = models.CharField(max_length=300,null=True,verbose_name='Observacao',blank=True)
    def __str__(self):
        return str(self.nm)
    class Meta:
        verbose_name='Irmão'

class irmaosLista(irmaos):
    class Meta:
        proxy=True
        verbose_name = 'Irmãos - listagem simple'


class dias(models.Model):
    p = 'Par'
    i = 'Impar'
    n = 'Nulo'
    adv = (
              (p,'Par'),
              (i,'Impar'),
              (n,'Nulo'),
    )
    seg = 'Segunda-feira'
    ter = 'Terca-feira'
    qua = 'Quarta-feira'
    qui = 'Quinta-feira'
    sex = 'Sexta-feira'
    sab = 'Sabado'
    dom = 'Domingo'
    dias_semana = (
        (seg,'Segunda-feira'),
        (ter,'Terca-feira'),
        (qua,'Quarta-feira'),
        (qui,'Quinta-feira'),
        (sex,'Sexta-feira'),
        (sab,'Sabado'),
        (dom,'Domingo'),
    )
    id = models.AutoField(primary_key=True)
    dia_semana = models.CharField(verbose_name='dia da semana',max_length=25,choices=dias_semana)
    irmao = models.ForeignKey(irmaos,on_delete=models.CASCADE,verbose_name='Nome do irmao',default=1)
    p1= models.BooleanField(default=False,verbose_name='Periodo 1')
    p1_1= models.BooleanField(default=False,verbose_name='Periodo 1')
    p1_2= models.BooleanField(default=False,verbose_name='Periodo 1')
    p2= models.BooleanField(default=False,verbose_name='Periodo 2')
    p2_1= models.BooleanField(default=False,verbose_name='Periodo 2')
    p3= models.BooleanField(default=False,verbose_name='Periodo 3')
    p3_1= models.BooleanField(default=False,verbose_name='Periodo 3')
    p4= models.BooleanField(default=False,verbose_name='Periodo 4')
    p4_1= models.BooleanField(default=False,verbose_name='Periodo 4')
    p5= models.BooleanField(default=False,verbose_name='Periodo 5')
    p5_1= models.BooleanField(default=False,verbose_name='Periodo 5')
    adv = models.CharField(max_length=6,choices=adv,null=True,verbose_name='Par/Impar',default='Nulo')
    preferencial = models.BooleanField(default=False,verbose_name='Preferencial') #este campo identifica que o irmao tem prioridade para a data e periodo que ele e voluntario
    def __str__(self):
        return str(self.dia_semana)
    class Meta:
        verbose_name = 'Dia'
        verbose_name_plural = 'Dia'
