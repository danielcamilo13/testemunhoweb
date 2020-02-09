from django import forms
from cadastro.models import designacao,irmaos
from django.forms import widgets

class designacaoForms(forms.Form):
    ano = forms.CharField(label='Ano',required=False)
    mes = forms.ChoiceField(choices=((1,'Janeiro'),(2,'Fevereiro'),(3,'Março'),(4,'Abril'),(5,'Maio'),(6,'Junho'),(7,'Julho'),(8,'Agosto'),(9,'Setembro'),(10,'Outubro'),(11,'Novembro'),(12,'Dezembro')),required=False,initial='2',widget=forms.Select(attrs={'style': 'border-color: blue;','placeholder': 'defina o mes na pesquisa'}))
    tpPesquisa = forms.ChoiceField(choices=((1,'tabela completa'),(2,'filtrar por nome')),label='Tipo Pesquisa',initial='filtrar por nome',required=False,widget=forms.Select(attrs={'style': 'border-color: orange;'}),)
    sel_irmaos = forms.ModelChoiceField(queryset=irmaos.objects.all().filter(habilitado='True').order_by('nm'),required=False,label='selecione o Irmao',widget=forms.Select(attrs={'style': 'border-color: orange;'}),)


