from django.conf.urls import url
from django.urls import path
from .agenda import EventFeed
from . import views

app_name = 'consulta'

urlpatterns =[
    #path('',views.index,name='index'),
    path('',views.consulta_designacao,name='consulta_designacao'),
    path('consulta_dia/',views.consulta_dia,name='consulta_dia'),
    path('consulta_designacao/',views.consulta_designacao,name='consulta_designacao'),
    path('retorno_designacao/',views.retorno_designacao,name='retorno_designacao'),
    path('resultado/',views.resultado,name='resultado'),
    path('agenda/evento.ics',EventFeed()),
    path('retorno/',views.scheduler,name='scheduler')
]