from django.urls import path
from . import views

app_name = 'cadastro'
urlpatterns =[
    path('',views.index,name='index'),
    path('designar/',views.designar,name='designar'),
    path('gerador/',views.gerador,name='gerador'),
    path('showing/',views.showing,name='showing'),
    path('confirmacao/',views.confirmacao,name='confirmacao'),
    path('importar/',views.importar,name='importar')
]