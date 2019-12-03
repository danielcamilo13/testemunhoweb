from django.conf.urls import url
from django.urls import path
from . import views
app_name = 'consulta'

urlpatterns =[
    path('',views.index,name='index'),
    path('resultado/',views.consulta,name='consulta')
]