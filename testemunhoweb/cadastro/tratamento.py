import os,sys,re
from .models import irmaos,dias
from openpyxl import load_workbook,Workbook
from django.core.files.storage import FileSystemStorage

def tratamento(dia,dm,ds,par,fill_header,designado_dia):
    '''
    ==> Tratamento das seguintes excessoes
    Excecao para com dia
    Prioridade no dia
    trio
    Excecao para com nome
    '''
    designado_dia = []
    irmaos = consulta_irmaos_dia_semana(ds)
    print('%s Tratamento de excecoes %s'%('*'*20,'*'*20))
    print('tratando o dia {}.{}'.format(dm,ds))
    print('campos prenchidos do dicionario dia {}'.format(dia))
    for irmao in irmaos:
        if irmao['preferencial']==True and not re.search(str(dm),str(irmao['irmao__excecao_dia'])):
            print('=====>Irmaos {} e preferencial na {}'.format(irmao['irmao__nm'],irmao['dia_semana']))
            print('Nao foi detectado nenhuma excecao adicional considerando o dia  {}. Dias de excecoes  {}'.format(dm,irmao['irmao__excecao_dia']))
            for k,v in sorted(irmao.items()):
                if k in dia and irmao['irmao__nm'] not in designado_dia and v==True:
                    print('ADICIONADO pois ele nao esta nas restricoes {}'.format(irmao['irmao__nm']))
                    designado_dia.append(irmao['irmao__nm'])
                    dia[k]=irmao['irmao__nm']


def consulta_irmaos_dia_semana(ds):
    orm_dia = dias.objects.select_related('irmao').values('dia_semana','irmao','irmao__nm','p1','p2','p3','p4','p5','p1_1','p1_2','p2_1','p3_1','p4_1','p5_1','irmao__habilitado','irmao__estado_civil','irmao__conjuge','irmao__gr','adv','irmao__maximo','preferencial','irmao__trio','irmao__privilegio','irmao__dianteira','irmao__excecao_dia','irmao__excecao_nome').filter(irmao__habilitado='True',dia_semana=ds).order_by('?')
    return orm_dia

def consulta_irmao_dia():
    orm_dia = dias.objects.select_related('irmao').values('dia_semana','irmao','irmao__nm','p1','p2','p3','p4','p5','p1_1','p1_2','p2_1','p3_1','p4_1','p5_1','irmao__habilitado','irmao__estado_civil','irmao__conjuge','irmao__gr','adv','irmao__maximo','preferencial','irmao__trio','irmao__privilegio','irmao__dianteira','irmao__excecao_dia','irmao__excecao_nome').filter(irmao__habilitado='True').order_by('-dia_semana')
    return orm_dia

def spreadsheet_reader(spreadsheet):
    data = []
    lines=[]
    wb = load_workbook(filename=spreadsheet)
    ws = wb.active
    last_row = ws.max_row
    last_column = ws.max_column
    print('Ultima Linha {} - Ultima coluna {}'.format(last_row,last_column))

    # for tt in range(1,ws.max_column):
    #     print('titulo {}'.format(tt))
    #     print(ws.cell(row=1,column=tt).value)
    for r in range(1,last_row):
        for c in range(1,last_column):
    #         # ln = ws.cell(row=1,column=c).value
            v = ws.cell(row=r,column=c).value
            if v is not None:
                lines.append(v)
                data.append(lines)
                print('dados %s'%data)
            # print(ws.cell(row=r,column=c).value)
            # data.append[ws.cell(row=r,column=c).value]
            # if ws.cell(row=r,column=c).value is not None:
            # print(ws.cell(row=r,column=c).value)
            # print('coluna 1 {},'.format(ws.cell(row=r,column=1).value))
            # print('coluna 2 {}'.format(ws.cell(row=r,column=2).value))
            # print('coluna 9 {}'.format(ws.cell(row=r,column=9).value))
            # nome = ws.cell(row=r,column=1).value
            # cidade = ws.cell(row=r,column=2).value
            # comprador = ws.cell(row=r,column=9).value
            # data.append[({'nome':nome,'cidade':cidade,'comprador':comprador})]
            # print('dados {}'.format(data))
    print('dados antes da inserção {}'.format(data))
    return data
