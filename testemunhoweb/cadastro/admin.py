# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time
from django.contrib import admin
from .models import irmaos,dias,irmaosLista,designacao
from django.utils import timezone
from .exporting import newEvent
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
import dateutil.rrule as rrule
from django.core import serializers
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER,TA_JUSTIFY
from io import BytesIO
from .exporting import EventFeed
# import pdfkit,tempfile,zipfile,time desativado momentaneamente pois estou usando o reportlab para gerar PDFs


def make_pdf(self,request,queryset):
    response = HttpResponse(content_type='application/pdf')
    pdffile = 'testemunho{0}.pdf'.format(time.strftime('%d-%m-%Y'))
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(pdffile)
    valores=[]
    buff = BytesIO()
    doc = SimpleDocTemplate(buff, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=60, bottomMargin=18)
    styles = getSampleStyleSheet()
    designacoes = []
    header = Paragraph("Minhas Designacoes", styles["Heading1"])
    designacoes.append(header)
    campos = [f.name for f in designacao._meta.get_fields()][3:]
    print('estes são os campos %s'%campos)
    valores.append(campos)
    for v in queryset:
        valores+=[str(v.mes),str(v.dia_mes),str(v.dia_semana),str(v.p1),str(v.p1_1),str(v.p1_2),str(v.p2),str(v.p2_1),str(v.p3),str(v.p3_1),str(v.p4),str(v.p4_1),str(v.p5),str(v.p5_1)],
    print(valores)
    t = Table(valores)
    t.setStyle(
        TableStyle([
                ('GRID', (0, 0), (-1, -1), 1, colors.dodgerblue),
                ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
                ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue),
                ('ALIGN',(0,-1),(-1,-1),'CENTER'),
                ('BOX', (0,0), (-1,-1), 0.20, colors.black),
                ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
                ]))
    designacoes.append(t)
    doc.build(designacoes)
    response.write(buff.getvalue())
    buff.close()
    self.message_user(request, 'arquivo gravado no caminho %s' % str(pdffile))
    return response

def schedule(self,request,queryset):
    bla = 0
    EventFeed()
    response = HttpResponse(content_type='text/calendar')
    serializers.serialize('xml',queryset,stream=response)
    # return HttpResponseRedirect('novoevento/',EventFeed())
    return response
    # response = HttpResponse(content_type='application/force-download')
    # ics = 'testemunho{0}.ics'.format(time.strftime('%d-%m-%Y'))
    # response['Content-Disposition'] = 'attachment;filename="{0}"'.format(ics)
    # self.message_user(request,' %s Mensagem de teste do ICS sem implementação'%(queryset))
    # return response

def set_irmao(self,request,queryset):
    updating = queryset.update(habilitado=True)
    mes = '%s registros '%updating
    self.message_user(request, '%s foram atualizadas.'%mes)

def unset_irmao(self,request,queryset):
    updating = queryset.update(habilitado=False)
    mes = '%s registros '%updating
    self.message_user(request, '%s foram atualizadas.'%mes)

set_irmao.short_description='Habilitar irmão'
unset_irmao.short_description='Desabilitar irmão'
schedule.short_description='Exportar designações para calendário'
make_pdf.short_description='Gerar arquivo PDF'

class diaItem(admin.TabularInline):
    model = dias
    def get_extra(self,request,obj=None,**kwargs):
        extra = 1
        return extra

class irmaoAdminlist(admin.ModelAdmin):
    list_display = ['nm','privilegio','dianteira']
    ordering = ['nm',]

class designacaoAdmin(admin.ModelAdmin):
    list_display = ['ano','mes','dia_mes','dia_semana','p1','p1_1','p1_2','p2','p2_1','p3','p3_1','p4','p4_1','p5','p5_1']
    list_filter = ['ano','mes']
    search_fields = ['p1','p1_1','p1_2','p2','p2_1','p3','p3_1','p4','p4_1','p5','p5_1',]
    actions=[schedule,make_pdf]

class irmaoAdmin(admin.ModelAdmin):
    list_display =['nm','conjuge','bairro','estado_civil','dianteira','privilegio','grupo','habilitado','maximo','dtModificado','obs']
    fieldsets = (('Dados do Irmao(a)',
                    {'fields':(('nm',),
                        ('nm_completo','gr'),
                        ('estado_civil','conjuge'),
                        ('grupo','cgcao'),
                        ('obs'),('dtModificado'))}),
                ('Endereço',
                    {'fields':(('endereco','bairro','telefone1','telefone2','email'),)}),
                ('Usado na definicao de designacao',
                    {'fields':(('habilitado','dianteira','privilegio','trio','maximo'),)}),
                ('adicional',
                    {'classes':('collapse',),
                            'fields':('excecao_nome','excecao_dia',),
                            })
                )
    inlines = [diaItem]
    search_fields = ['nm',]
    actions = [set_irmao,unset_irmao,schedule]
    ordering = ['nm',]
    save_on_top=True
    view_on_site = True
    list_filter=('dianteira','privilegio','bairro')
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        # retorno = form.cleaned_data.get('dtModificado')
        if change:
            obj.dtModificado = timezone.now()
        obj.save()

admin.site.register(irmaos,irmaoAdmin)
admin.site.register(irmaosLista,irmaoAdminlist)
admin.site.register(designacao,designacaoAdmin)