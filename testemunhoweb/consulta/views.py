# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from cadastro.tratamento import consulta_irmaos_dia_semana
from cadastro.models import designacao,irmaos
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from consulta.forms import designacaoForms
from django.utils import timezone
from datetime import datetime
from django.db.models import Q
import calendar,locale
from .agenda import EventFeed
from icalendar import Calendar,Event

def index(request):
    aviso = 'aviso'
    return render(request,'consulta/index.html')

def consulta_dia(request):
    return render(request,'consulta/consulta_dia.html')

def consulta_designacao(request):
    locale.setlocale(locale.LC_ALL,'pt_BR.UTF-8')
    usuario = request.user.groups.values_list('name',flat=True)
    print(usuario)
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
        if p=='1': #Pesquisa completa
            mensagem = {'completa':'Tipo de Pesquisa - COMPLETA'}
            form_retorno = designacao.objects.values().filter(ano=a,mes=mes).order_by('ano','mes','dia_mes','dia_semana')
            return render(request, 'consulta/retorno_designacao.html', {'form_retorno': form_retorno,'mensagem':mensagem})
        elif p=='2':  #Pesquisa por Irmao
            if len(irmao)<1:
                mensagem = {'pessoa':'favor definir o irmao'}
                form_retorno = designacao.objects.values().filter(Q(p1=i)|Q(p1_1=i)|Q(p1_2=i)|Q(p2=i)|Q(p2_1=i)|Q(p3=i)|Q(p3_1=i)|Q(p4=i)|Q(p4_1=i)|Q(p5=i)|Q(p5_1=i),ano=a,mes=mes).order_by('ano','mes','dia_mes','dia_semana')
            else:
                mensagem = {'irmao':'Nome do irmao selecionado %s'%str(i)}
                form_retorno = designacao.objects.values().filter(Q(p1=i)|Q(p1_1=i)|Q(p1_2=i)|Q(p2=i)|Q(p2_1=i)|Q(p3=i)|Q(p3_1=i)|Q(p4=i)|Q(p4_1=i)|Q(p5=i)|Q(p5_1=i),ano=a,mes=mes).order_by('ano','mes','dia_mes','dia_semana')
            return render(request,'consulta/retorno_designacao.html',{'form_retorno':form_retorno,'mensagem':mensagem})
            # return JsonResponse(form_retorno,safe=False)
    else:
        mensagem = {'semretorno':'sem resposta'}
        return render(request,'consulta/retorno_designacao',{'mensagem':mensagem})

def resultado(request):
    if 'dia' in request.POST:
        d = str(request.POST['dia'])
        irmaos = consulta_irmaos_dia_semana(d)
    return render(request, 'consulta/resultado.html',{'irmaos':irmaos})

def scheduler(request):
    sch = EventFeed()
    print(sch)
    print(sch.items)
    print(sch.item_description)
    myDict = {k: list(request.POST.getlist(k))[c] for k, v in request.POST.items() if k != 'csrfmiddlewaretoken'}
    print(myDict)
    if 'mes' in request.POST:
        print('homenagem')
    if request.method=='POST':
        for k,v in request.POST.items():
            print('item {}'.format(k,v))
            for l in request.POST.getlist(k):
                print('valores dos items: %s'%l)

    else:
        print('nao ha post')
    # return HttpResponse('o que vai volta')
    data = {'1':'valor 1','2':'valor 2'}
    return JsonResponse(data,safe=False)

    # dia = datetime.now()
    # cal = Calendar()
    # cal.add('prodid', '-//%s Events Calendar//%s//' % ('nome', 'dominio'))
    # cal.add('version', '2.0')
    #
    # # site_token = site.domain.split('.')
    # # site_token.reverse()
    # # site_token = '.'.join(site_token)
    #
    # ical_event = Event()
    # ical_event.add('summary', 'sumario')
    # ical_event.add('dtstart', dia)
    # ical_event.add('dtend', dia)
    # ical_event.add('dtstamp', dia)
    # # ical_event['uid'] = '%d.event.events.%s' % (event.id, site_token)
    # cal.add_component(ical_event)
    #
    # response = HttpResponse(mimetype="text/calendar")
    # response['Content-Disposition']='attachment;filename=%s.ics'%event.slug
    # return response