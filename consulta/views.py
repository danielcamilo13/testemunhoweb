# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# from django.conf import settings
# from django.contrib.sites.models import Site
from cadastro.tratamento import consulta_irmaos_dia_semana
from cadastro.models import designacao,irmaos
#from calendario.models import calendario
from django.shortcuts import render, redirect, get_object_or_404,render_to_response
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.template import RequestContext
from django.middleware import csrf
from consulta.forms import designacaoForms
from django.utils import timezone
from datetime import datetime
from django.db.models import Q
from django_ical.views import ICalFeed

from .agenda import EventFeed
from urllib.request import urlopen
from bs4 import BeautifulSoup
from django_ical import feedgenerator
from django.template.defaultfilters import slugify
import calendar,locale, requests,csv,json,os,vobject,time,pytz,re
from icalendar import Calendar, Event
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.views.generic import View

from .tratamento import make_pdf

def index(request):
    aviso = 'aviso'
    return render(request,'consulta/index.html')

def consulta_dia(request):
    return render(request,'consulta/consulta_dia.html')

def consulta_designacao(request):
    locale.setlocale(locale.LC_ALL,'pt_BR.UTF-8')
    grupo = request.user.groups.values_list('name',flat=True)

    hoje = timezone.now()
    m = hoje.month
    a = hoje.year
    if request.method=='POST':
        form = designacaoForms(request.POST)
        return render(request,'consulta/consulta_designacao.html',{'form':form,'grupo':grupo})
    else:
        form = designacaoForms(initial={'ano':int(a),'mes':m})
        return render(request,'consulta/consulta_designacao.html',{'form':form,'grupo':grupo})

def retorno_designacao(request):
    locale.setlocale(locale.LC_ALL,'pt_BR.UTF-8')
    BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    BASE_DIR = os.path.join(BASE,'medias')
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
            form = designacao.objects.values().filter(ano=a,mes=mes).order_by('ano','mes','dia_mes','dia_semana')
            return render(request, 'consulta/retorno_designacao.html', {'form': form,'mensagem':mensagem})
        elif p=='2':  #Pesquisa por Irmao
            if len(irmao)<1:
                mensagem = {'pessoa':'favor definir o irmao'}
                form = designacao.objects.values().filter(Q(p1=i)|Q(p1_1=i)|Q(p1_2=i)|Q(p2=i)|Q(p2_1=i)|Q(p3=i)|Q(p3_1=i)|Q(p4=i)|Q(p4_1=i)|Q(p5=i)|Q(p5_1=i),ano=a,mes=mes).order_by('ano','mes','dia_mes','dia_semana')
            else:
                mensagem = {'irmao':str(i)}
                form = designacao.objects.values().filter(Q(p1=i)|Q(p1_1=i)|Q(p1_2=i)|Q(p2=i)|Q(p2_1=i)|Q(p3=i)|Q(p3_1=i)|Q(p4=i)|Q(p4_1=i)|Q(p5=i)|Q(p5_1=i),ano=a,mes=mes).order_by('ano','mes','dia_mes','dia_semana')
                f_filter = [ {f['ano'],f['mes'],f['dia_semana'],f['dia_mes']} for f in form]
                contexto = form
                ctxt_periodos =[]
                ctxt_periodos_filtro = []
                for ln in contexto:
                    mes = time.strptime(ln['mes'], "%B").tm_mon
                    day_b = '{}-{}-{}'.format(ln['dia_mes'],mes,ln['ano'])
                    day_a = datetime.strptime(day_b,'%d-%m-%Y')
                    ctxt = {i:{'dia':str(day_a),'semana':ln['dia_semana'],
                            'periodo1':[ln['p1'],ln['p1_1'],ln['p1_2']],
                            'periodo2':[ln['p2'],ln['p2_1']],
                            'periodo3':[ln['p3'],ln['p3_1']],
                            'periodo4':[ln['p4'],ln['p4_1']],
                            'periodo5':[ln['p5'],ln['p5_1']]}}
                    ctxt_periodos.append(ctxt)
                #abrir a lista gerada e na lista foi feito um IF com a chave principal e os conteudos se igualarem
                for linhas in ctxt_periodos:
                    for ch,valores in linhas.items():
                        f = [{k:v} for k,v in valores.items() if k=='dia' or k=='semana' or re.search(i,str(v))]
                        ctxt_periodos_filtro.append(f)
                            
                with open(os.path.join(BASE_DIR,'calendario.json'),'w') as fl:
                    json.dump(ctxt_periodos,fl,indent=4)
            form_filtro = ctxt_periodos_filtro
            return render(request,'consulta/retorno_designacao.html',{'form_filtro':form_filtro,'mensagem':mensagem})
    else:
        mensagem = {'semretorno':'sem resposta'}
        return render(request,'consulta/retorno_designacao',{'mensagem':mensagem})

def resultado(request):
    if 'dia' in request.POST:
        d = str(request.POST['dia'])
        irmaos = consulta_irmaos_dia_semana(d)
    return render(request, 'consulta/resultado.html',{'irmaos':irmaos})


# def make_calendar_object(event_id):
#     event = get_object_or_404(calendario, pk=id)
#
#     site = Site.objects.get_current()
#
#     site_token = site.domain.split('.')
#     site_token.reverse()
#     site_token = '.'.join(site_token)
#
#     cal = Calendar()
#     cal.add('prodid', '-//%s Events Calendar//%s//' % (site.name, site.domain))
#     cal.add('version', '2.0')
#
#     eventObj = Event()
#     eventObj.add('summary', event.name)
#     eventObj.add('location', event.location)
#     eventObj.add('dtstart', event.start_datetime)
#     eventObj.add('dtend', event.end_datetime)
#     eventObj.add('dtstamp', event.created_datetime)
#     eventObj['uid'] = '%dT%d.events.%s' % (event.id, random.randrange(111111111, 999999999), site_token)
#     eventObj.add('priority', 5)
#
#     cal.add_component(eventObj)
#
#     output = ""
#     for line in cal.content_lines():
#         if line:
#             output += line + "\n"
#     return output


def create_ics(data):
    cal = vobject.iCalendar()
    utc = vobject.icalendar.utc
    d = datetime.strptime(data['dia'],'%Y-%m-%d %H:%M:%S')
    dia_agenda = datetime(d.year, d.month, d.day,tzinfo=utc)
    cal.add('method').value = 'PUBLISH'
    vevent = cal.add('vevent')
    start = cal.vevent.add('dtstart')
    start.value = datetime(d.year,d.month,d.day,tzinfo=utc)
    sum = cal.vevent.add('summary')
    sum.value= data['tp']
    desc = cal.vevent.add('description')
    desc.value = data['periodo']
    return cal.serialize()
    #cal.add('method').value = 'PUBLISH'
    #vevent = cal.add('vevent')
    #vevent.add('dtstart').value = '20050404T080000'
    ##vevent.add('dtstart').value = dia_agenda
    #vevent.add('dtend').value = dia_agenda
    #vevent.add('dtstamp').value = dia_agenda
    #vevent.add('summary').value = 'Testemunho publico - minha designacao'


    
def scheduler(request):
    if request.method=='POST':
        print(request.session)
    BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    BASE_DIR = os.path.join(BASE,'medias')
    #context = RequestContext(request)
    lista_calendario = []
    todos_agendamentos=''
    with open(os.path.join(BASE_DIR,'calendario.json')) as fl:
        calendario = json.load(fl)
        for irmao in calendario:
            for k,pers in irmao.items():
                print('Irmao {}'.format(k))
                sel = k
                for per,val in pers.items():
                    print('Periodo {}'.format(per,val))
                    if per =='dia':
                        dd=val
                    if re.search(sel,str(val)):
                        print('registro localizado {}'.format(val))
                        contexto={'dia':dd,'tp':'Testemunho publico - designacao de '+str(sel),'periodo':str(per)+'='+str(val[0])}
                        lista_calendario.append(contexto)

    if isinstance(lista_calendario,list):
        for item in lista_calendario:
            grava_calendario = create_ics(item)
            todos_agendamentos+=grava_calendario
            print('gravar no calendario {}'.format(grava_calendario))

        response = HttpResponse(todos_agendamentos,content_type='text/calendar')
        response['Filename']=os.path.join(BASE_DIR,'calendario_hoje.ics')
        response['Content-Disposition']='attachment;filename=filename.ics'
    return response
    
    #if request.method=='POST':
    #    print('retorno POST com sucesso')
    #    print('post: %s'%request.POST)
    #    print('Sessao %s'%request.session)
    #    return render(request,"consulta/retorno.html",{'lista_calendario':lista_calendario})
    #else:
    #    return render_to_response("consulta/retorno.html", context_dict, context)

def gerar_pdf(request):
    BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    BASE_DIR = os.path.join(BASE,'medias')
    #context = RequestContext(request)
    lista_calendario = []
    todos_agendamentos=''
    with open(os.path.join(BASE_DIR,'calendario.json')) as fl:
        calendario = json.load(fl)
        for irmao in calendario:
            for k,pers in irmao.items():
                print('Irmao {}'.format(k))
                sel = k
                for per,val in pers.items():
                    print('Periodo {}'.format(per,val))
                    if per =='dia':
                        dd=val
                    if re.search(sel,str(val)):
                        print('registro localizado {}'.format(val))
                        contexto={'dia':dd,'tp':'Testemunho publico - designacao de '+str(sel),'periodo':str(per)+'='+str(val[0])}
                        lista_calendario.append(contexto)
    print('Lista de calendários {}'.format(lista_calendario))
    #gerando_pdf=make_pdf()
    return HttpResponse('atenção')

def ajax_test(request):
    context={'ajax','retorno de ajax'}
    return render(request,'consulta/placed.html',{'context':context})