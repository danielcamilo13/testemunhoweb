# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import irmaos,dias,irmaosLista
from django.utils import timezone

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

class diaItem(admin.TabularInline):
    model = dias
    def get_extra(self,request,obj=None,**kwargs):
        extra = 1
        return extra

class irmaoAdminlist(admin.ModelAdmin):
    list_display = ['nm','privilegio','dianteira']
    ordering = ['nm',]


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
    actions = [set_irmao,unset_irmao]
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

    # def save_model(self, request, obj, form, change):
    #
    #     obj.save
    #     if form.changed_data == True:
    #         self.cleaned_data['dtModificado']=timezone.now
    #         form.save
    #
    #     super(irmaoAdmin,self).save_model(request,obj,form,change)

    # fieldsets=(('Dados da Costureira',{'fields':(('nm_costureira','cpf'),('rota','endereco','num','complemento'),('bairro','cep','cidade','estado'),('ddd1','fone1','ddd2','fone2'),('contato','email'))}),
    # ('Informação adicional',{'classes':('collapse',),'fields':(('nr_banco','banco','tp_conta','agencia','nr_conta'),'status','obs'),}),)

admin.site.register(irmaos,irmaoAdmin)
admin.site.register(irmaosLista,irmaoAdminlist)
admin.site.register(dias)