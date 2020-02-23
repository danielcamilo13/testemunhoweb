# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# from django.conf import settings
# from django.contrib.sites.models import Site
from cadastro.tratamento import consulta_irmaos_dia_semana
from cadastro.models import designacao,irmaos
from calendario.models import calendario
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
import calendar,locale, requests,csv,json,os,vobject,time,pytz
from icalendar import Calendar, Event
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.views.generic import View

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
            form_retorno = designacao.objects.values().filter(ano=a,mes=mes).order_by('ano','mes','dia_mes','dia_semana')
            return render(request, 'consulta/retorno_designacao.html', {'form_retorno': form_retorno,'mensagem':mensagem})
        elif p=='2':  #Pesquisa por Irmao
            if len(irmao)<1:
                mensagem = {'pessoa':'favor definir o irmao'}
                form_retorno = designacao.objects.values().filter(Q(p1=i)|Q(p1_1=i)|Q(p1_2=i)|Q(p2=i)|Q(p2_1=i)|Q(p3=i)|Q(p3_1=i)|Q(p4=i)|Q(p4_1=i)|Q(p5=i)|Q(p5_1=i),ano=a,mes=mes).order_by('ano','mes','dia_mes','dia_semana')
            else:
                mensagem = {'irmao':'Nome do irmao selecionado %s.'%str(i)}
                form_retorno = designacao.objects.values().filter(Q(p1=i)|Q(p1_1=i)|Q(p1_2=i)|Q(p2=i)|Q(p2_1=i)|Q(p3=i)|Q(p3_1=i)|Q(p4=i)|Q(p4_1=i)|Q(p5=i)|Q(p5_1=i),ano=a,mes=mes).order_by('ano','mes','dia_mes','dia_semana')
                contexto = list(form_retorno)
                contexto_periodos =[]
                for ln in contexto:
                    mes = time.strptime(ln['mes'], "%B").tm_mon
                    day_b = '{}-{}-{}'.format(ln['dia_mes'],mes,ln['ano'])
                    day_a = datetime.strptime(day_b,'%d-%m-%Y')
                    ctxt = {'dia':str(day_a),'semana':ln['dia_semana'],
                            'periodo1':[ln['p1'],ln['p1_1'],ln['p1_2']],
                            'periodo2':[ln['p2'],ln['p2_1']],
                            'periodo3':[ln['p3'],ln['p3_1']],
                            'periodo4':[ln['p4'],ln['p4_1']],
                            'periodo5':[ln['p5'],ln['p5_1']]}
                    contexto_periodos.append(ctxt)

                with open(os.path.join(BASE_DIR,'calendario.json'),'w') as fl:
                    json.dump(contexto_periodos,fl,indent=4)
            return render(request,'consulta/retorno_designacao.html',{'form_retorno':form_retorno,'mensagem':mensagem})
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
    #locale.setlocale(locale.LC_ALL,'pt_BR.UTF-8')
    cal = vobject.iCalendar()
    utc = vobject.icalendar.utc
    d = datetime.strptime(data['dia'],'%Y-%m-%d %H:%M:%S')
    print('dia {} mes {} ano {} '.format(d.day,d.month,d.year))
    dia_agenda = datetime(d.year, d.month, d.day,tzinfo=utc)
    #dia_agenda = datetime(data['dia'].year, data['dia'].month, data['dia'].day, tzinfo = utc)
    print('variavel dia agenda {}'.format(dia_agenda))
    vevent = cal.add('vevent')
    start = cal.vevent.add('dtstart')
    #start.value = datetime(2006, 2, 16, tzinfo = utc)
    start.value = datetime(d.year,d.month,d.day,tzinfo=utc)
    sum = cal.vevent.add('summary')
    sum.value= data['tp']
    desc = cal.vevent.add('description')
    desc.value = 'valor da descricao'
    #desc.value = data['periodo1']
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
        print(request.POST.getlist('dia'))
    BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    BASE_DIR = os.path.join(BASE,'medias')
    #context = RequestContext(request)
    #context_dict = {}
    lista_calendario = []
    todos_agendamentos=''
    #contexto = {}
    with open(os.path.join(BASE_DIR,'calendario.json')) as fl:
        calendario = json.load(fl)
        for ln in calendario:
            contexto={'dia':ln['dia'],'tp':'Testemunho publico - minha designacao','periodo1':ln['periodo1']}
            lista_calendario.append(contexto)

    if isinstance(lista_calendario,list):
        for item in lista_calendario:
            grava_calendario = create_ics(item)
            todos_agendamentos+=grava_calendario
            print('gravar no calendario {}'.format(grava_calendario))
            print('gravar no calendario {}'.format(type(grava_calendario)))

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

