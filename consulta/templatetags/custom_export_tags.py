from django import template
from cadastro.models import designacao
from django.utils import timezone

register = template.Library()

@register.filter
def export(retorno):
    data = 'valor de retorno'
    return data