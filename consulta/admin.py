# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import consulta
from django.contrib import admin
#from .forms import designacaoForms
from django.urls import path
from django.utils import timezone
from django.shortcuts import render
#from consulta.forms import designacaoForms

class consultaAdmin(admin.ModelAdmin):
    pass
#    """A ModelAdmin that uses a different form class when adding an object."""
#    def get_form(self, request, obj=None, **kwargs):
#        if obj is None:
#            return designacaoForms
#        else:
#            return super(consultaAdmin, self).get_form(request, obj, **kwargs)

#class CustomAdminSite(admin.AdminSite):
  
#    def get_urls(self):
#        urls = super(CustomAdminSite, self).get_urls()
#        custom_urls = [
#            url(r'desired/path$', self.admin_view(organization_admin.preview), name="preview"),
#        ]
#        return urls + custom_urls

#class consultaAdmin(admin.ModelAdmin):
#     def get_urls(self):
#        urls = super().get_urls()
#        my_urls = [
#            path('consulta/', self.admin_site.admin_view(self.))
#        ]
#        return my_urls + urls
    #hoje = timezone.now()
    #m = hoje.month
    #a = hoje.year
    #form = designacaoForms(initial={'ano':int(a),'mes':m})
    #change_form_template='consulta/minha_designacao.html'
    #def change_view(self, request, object_id, form_url='', extra_context=None):
    #    extra_context = extra_context or {}
    #    extra_context['osm_data'] = self.get_osm_info()
    #    return super().change_view(
    #        request, object_id, form_url, extra_context=extra_context,
    #    )

admin.site.register(consulta,consultaAdmin)
