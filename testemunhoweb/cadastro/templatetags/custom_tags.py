from django import template
from cadastro.models import designacao
from django.utils import timezone
import calendar,locale

register = template.Library()

@register.filter
def next(value):
    locale.setlocale(locale.LC_ALL,'pt_BR.UTF-8')
    hoje = timezone.now()
    d=hoje.day+1
    m = hoje.month
    a = hoje.year
    mes = calendar.month_name[m]
    prox_dias = designacao.objects.values().filter(dia_mes=d,mes=mes)
    prox_dia=''
    for dia in prox_dias:
        prox_dia+='Mes: '+dia['mes']+' Dia: '+str(dia['dia_mes'])+' - '+dia['dia_semana']+'. Horario 1: '+dia['p1']+' '+dia['p1_1']+''+dia['p1_2']+'. Horario 2: '+dia['p2']+' '+dia['p2_1']+''+dia['p3']+''+dia['p3_1']+'. Horario 3: '+dia['p4']+' '+dia['p4_1']+'. Horario 4: '+dia['p5']+' '+dia['p5_1']
    return prox_dia

#@register.inclusion_tag('consulta.html')
#def any_function():
#    variable = designacao.objects.count()
#    return {'variable': variable}

#@register.
#def any_function(count=5):
    #return designacao.objects.count()