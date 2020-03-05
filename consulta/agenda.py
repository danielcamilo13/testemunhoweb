from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from django_ical.views import ICalFeed
from cadastro.models import designacao
#from calendario.models import calendario


class EventFeed(ICalFeed):
    """
    A simple event calender
    """
    product_id = '-//example.com//Example//EN'
    timezone = 'UTC'
    file_name = "evento.ics"

    def items(self):
        return calendario.objects.all().order_by('-data_inicial')

    def item_guid(self, item):
        return "{}{}".format(item.id, "global_name")

    def item_title(self, item):
        return "{}".format(item.titulo)

    def item_description(self, item):
        return item.descricao

    def item_start_datetime(self, item):
        return item.data_inicial

    def item_link(self, item):
        return "http://www.google.de"
    def file_name(self,obj):
        return 'feed_%s'%obj.id


'''
class EventFeed(ICalFeed):
    """
    A simple event calender
    """
    product_id = '-//example.com//Example//EN'
    timezone = 'UTC'
    file_name = "event.ics"

    def file_name(self, obj):
        return "feed_%s.ics" % obj.id

    def items(self):
        return designacao.objects.all().order_by('-dia_mes')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_start_datetime(self, item):
        return item.start_datetime

    def item_rrule(self, item):
        """Adapt Event recurrence to Feed Entry rrule."""
        if item.recurrences:
            rules = []
            for rule in item.recurrences.rrules:
                rules.append(build_rrule_from_recurrences_rrule(rule))
            return rules

    def item_exrule(self, item):
        """Adapt Event recurrence to Feed Entry exrule."""
        if item.recurrences:
            rules = []
            for rule in item.recurrences.exrules:
                rules.append(build_rrule_from_recurrences_rrule(rule))
            return rules

    def item_rdate(self, item):
        """Adapt Event recurrence to Feed Entry rdate."""
        if item.recurrences:
            return item.recurrences.rdates

    def item_exdate(self, item):
        """Adapt Event recurrence to Feed Entry exdate."""
        if item.recurrences:
            return item.recurrences.exdates
'''

def index(request):
    print(request)
    return HttpResponse('Retorno do calendario index')
