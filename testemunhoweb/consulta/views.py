# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from cadastro.tratamento import consulta_irmaos_dia_semana
from cadastro.models import designacao,irmaos
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from consulta.forms import designacaoForms
from django.utils import timezone
from datetime import datetime
from django.db.models import Q
import calendar,locale

def index(request):
    aviso = 'aviso'
    return render(request,'consulta/index.html')

def consulta_dia(request):
    return render(request,'consulta/consulta_dia.html')

def consulta_designacao(request):
    locale.setlocale(locale.LC_ALL,'pt_BR.UTF-8')
    hoje = timezone.now()
    m = hoje.month
    a = hoje.year
    if request.method=='POST':
        form = designacaoForms(request.POST)
        return render(request,'consulta/consulta_designacao.html',{'form':form})
    else:
        form = designacaoForms(initial={'ano':int(a),'mes':m})
        return render(request,'consulta/consulta_designacao.html',{'form':form})

def retorno_designacao(request):
    if request.method=='POST':
        irmao = request.POST['sel_irmaos']
        m = int(request.POST['mes'])
        a = request.POST['ano']
        p = request.POST['tpPesquisa']
        mes = calendar.month_name[m]
        if len(irmao)==0:
            i=0
        else:
            i = [v['nm'] for v in irmaos.objects.values('nm').filter(pk=irmao)][0]
        if p=='1':
            print('Tabela completa')
            form_retorno = designacao.objects.values().filter(ano=a,mes=mes).order_by('ano','mes','dia_mes','dia_semana')
            return render(request, 'consulta/consulta_designacao.html', {'form_retorno': form_retorno})
        elif p=='2':
            print('Tabela por pessoa')
            form_retorno = designacao.objects.values().filter(Q(p1=i)|Q(p1_1=i)|Q(p1_2=i)|Q(p2=i)|Q(p2_1=i)|Q(p3=i)|Q(p3_1=i)|Q(p4=i)|Q(p4_1=i)|Q(p5=i)|Q(p5_1=i),ano=a,mes=mes).order_by('ano','mes','dia_mes','dia_semana')
            return render(request,'consulta/consulta_designacao.html',{'form_retorno':form_retorno})

def resultado(request):
    if 'dia' in request.POST:
        d = str(request.POST['dia'])
        irmaos = consulta_irmaos_dia_semana(d)
    return render(request, 'consulta/resultado.html',{'irmaos':irmaos})