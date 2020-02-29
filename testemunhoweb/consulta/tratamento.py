# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet

def make_pdf(self,request,queryset):
    response = HttpResponse(content_type='application/pdf')
    pdffile = 'testemunho{0}.pdf'.format(time.strftime('%d-%m-%Y'))
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(pdffile)
    valores=[]
    buff = BytesIO()
    doc = SimpleDocTemplate(buff, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=60, bottomMargin=18)
    styles = getSampleStyleSheet()
    designacoes = []
    header = Paragraph("Minhas Designacoes", styles["Heading1"])
    designacoes.append(header)
    # campos = [f.name for f in designacao._meta.get_fields()][3:] = extraindo o cabecalho
    campos=['mes','dia','semana','Per 1','Per 1','Per 1','Per 2','Per 2','Per 3','Per 3','Per 4','Per 4','Per 5','Per 5']
    # print('estes são os campos %s'%campos)
    valores.append(campos)
    for v in queryset:
        valores+=[str(v.mes),str(v.dia_mes),str(v.dia_semana),str(v.p1),str(v.p1_1),str(v.p1_2),str(v.p2),str(v.p2_1),str(v.p3),str(v.p3_1),str(v.p4),str(v.p4_1),str(v.p5),str(v.p5_1)],
    # print(valores)
    t = Table(valores)
    t.setStyle(
        TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.dodgerblue),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue),
            ('ALIGN',(0,-1),(-1,-1),'CENTER'),
            ('BOX', (0,0), (-1,-1), 0.20, colors.black),
            ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
        ]))
    designacoes.append(t)
    doc.build(designacoes)
    response.write(buff.getvalue())
    buff.close()
    self.message_user(request, 'arquivo gravado no caminho %s' % str(pdffile))
    return response
