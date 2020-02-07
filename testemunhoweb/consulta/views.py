# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from cadastro.tratamento import consulta_irmaos_dia_semana
from cadastro.models import designacao
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from consulta.forms import designacaoForms
from django.utils import timezone
from datetime import datetime

def index(request):
    aviso = 'aviso'
    return render(request,'consulta/index.html')

def consulta_dia(request):
    return render(request,'consulta/consulta_dia.html')

def consulta_designacao(request):
    if request.method=='POST':
        form = designacaoForms(request.POST)
        return render(request,'consulta/consulta_designacao.html',{'form':form})
    else:
        form = designacaoForms(request.POST)
        return render(request,'consulta/consulta_designacao.html',{'form':form})

def retorno_designacao(request):
    if request.method=='POST':
        form_retorno = designacao.objects.all().order_by('ano','mes','dia_mes','dia_semana')
    return render(request,'consulta/consulta_designacao.html',{'form_retorno':form_retorno})

def resultado(request):
    if 'dia' in request.POST:
        d = str(request.POST['dia'])
        irmaos = consulta_irmaos_dia_semana(d)
    return render(request, 'consulta/resultado.html',{'irmaos':irmaos})