from django.urls import path
from . import views

app_name = 'cadastro'
urlpatterns =[
    path('',views.index,name='index'),
    path('gerador/',views.generate,name='gerador'),
    path('showing/',views.showing,name='showing'),
    path('planilha/',views.planilha,name='planilha'),
]