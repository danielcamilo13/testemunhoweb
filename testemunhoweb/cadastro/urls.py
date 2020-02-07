from django.urls import path
from . import views
# from .exporting import EventFeed

app_name = 'cadastro'
urlpatterns =[
    #path('',views.designar,name='designar'),
    path('designar/',views.designar,name='designar'),
    path('gerador/',views.gerador,name='gerador'),
    path('showing/',views.showing,name='showing'),
    path('confirmacao/',views.confirmacao,name='confirmacao'),
    path('importar/',views.importar,name='importar'),
    # path('novoevento', EventFeed(),name='novoevento'),
]