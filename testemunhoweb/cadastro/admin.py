# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import irmaos,dias,irmaosLista,designacao
from django.utils import timezone
from .tratamento import newEvent
import dateutil.rrule as rrule

def make_pdf(self,request,queryset):
    bla = 0

def export_schedule(self,request,queryset):
    ev = newEvent()
    print(ev)
    self.message_user(request,' %s - %s Mensagem de retorno'%(ev,queryset))

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
export_schedule.short_description='Exportar designações'


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
    actions=[export_schedule]

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
    actions = [set_irmao,unset_irmao,export_schedule]
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