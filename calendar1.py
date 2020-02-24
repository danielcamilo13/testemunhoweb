import icalendar
import recurring_ical_events
import urllib.request

start_date = (2020, 1, 1)
end_date =   (2020, 4, 1)
url = "http://tinyurl.com/y24m3r8f"

ical_string = urllib.request.urlopen(url).read()
calendar = icalendar.Calendar.from_ical(ical_string)
events = recurring_ical_events.of(calendar).between(start_date, end_date)
for event in events:
    start = event["DTSTART"].dt
    duration = event["DTEND"].dt - event["DTSTART"].dt
    print("start {} duration {}".format(start, duration))