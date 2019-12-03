# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from cadastro.tratamento import consulta_irmaos_dia_semana
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect


def index(request):
	aviso = 'aviso'
	return render(request,template_name='consulta/index.html')

def consulta(request):
	if 'dia' in request.POST:
		d = str(request.POST['dia'])
		irmaos = consulta_irmaos_dia_semana(d)
	return render(request, 'consulta/resultado.html',{'irmaos':irmaos})

# render(request,'consulta/resultado.html',{'resposta':contexto})