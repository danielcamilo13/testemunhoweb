from django_ical.views import ICalFeed
from .models import designacao
from django_cal.views import Events
import dateutil.rrule as rrule
from django_ical.utils import build_rrule
from datetime import date

# Mapping of iCalendar event attributes to prettier names.
EVENT_ITEMS = (
    ('uid', 'item_uid'),
    ('dtstart', 'item_start'),
    ('dtend', 'item_end'),
    ('duration', 'item_duration'),
    ('summary', 'item_summary'),
    ('description', 'item_description'),
    ('location', 'item_location'),
    ('url', 'item_url'),
    ('comment', 'item_comment'),
    ('last-modified', 'item_last_modified'),
    ('created', 'item_created'),
    ('categories', 'item_categories'),
    ('rruleset', 'item_rruleset')
)

class EventFeed(ICalFeed):
    """
    A simple event calender
    """
    print('calling EventFeed sucessfully')
    product_id = '-//example.com//Example//EN'
    timezone = 'UTC'
    file_name = "event.ics"

    def file_name(self,obj):
        return 'feed_%s.ics'%obj
        # return 'feed_%s.ics'%obj.id

    def items(self):
        return designacao.objects.all().order_by('-dia_semana')

    def item_guid(self, item):
        return "{}{}".format(item.id, "dia")

    def item_title(self, item):
        return "{}".format(item.mes)

    def item_description(self, item):
        return item.dia_semana

    # def item_start_datetime(self, item):
    #     return item.mes
    def __call__(self, request, *args, **kwargs):
        response = super(EventFeed, self).__call__(request, *args, **kwargs)
        if response.mimetype == 'text/calendar':
            response['Filename'] = 'filename.ics'  # IE needs this
            response['Content-Disposition'] = 'attachment; filename=filename.ics'
        return response

    def item_link(self, item):
        return "http://www.google.de"

class newEvent(Events):
    def items(self):
        return ["Whattaday!", "meow"]

    def cal_name(self):
        return "a pretty calendar."

    def cal_desc(self):
        return "Lorem ipsum tralalala."

    def item_summary(self, item):
        return "That was suchaday!"

    def item_start(self, item):
        return datetime.date(year=2011, month=1, day=24)

    def item_end(self, item):
        return datetime.date(year=2011, month=1, day=26)

    def item_rruleset(self, item):
        rruleset = rrule.rruleset()
        # rruleset.rrule(rrule.YEARLY, count=10, dtstart=self.item_start(item))
        # rruleset.rrule(rrule.YEARLY, dtstart=self.item_start(item))
        return rruleset

    def item_categories(self, item):
        return ["Family", "Birthdays"]


