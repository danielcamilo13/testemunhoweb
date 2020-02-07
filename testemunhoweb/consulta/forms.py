from django import forms
from cadastro.models import designacao,irmaos
from django.forms import widgets

class designacaoForms(forms.Form):
    mes = forms.ChoiceField(choices=((1,'Janeiro'),(2,'Fevereiro'),(3,'Março'),(4,'Abril'),(5,'Maio'),(6,'Junho'),(7,'Julho'),(8,'Agosto'),(9,'Setembro'),(10,'Outubro'),(11,'Novembro'),(12,'Dezembro')),required=False)
    tpPesquisa = forms.ChoiceField(choices=((1,'tabela completa'),(2,'filtrar por nome')),label='Tipo de Pesquisa',initial='filtrar por nome',required=False)
    sel_irmaos = forms.ModelChoiceField(queryset=irmaos.objects.all().order_by('nm'),required=True,label='selecione o Irmao')

