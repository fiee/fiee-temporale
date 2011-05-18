import vobject
from datetime import datetime, timedelta #, time

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from temporale.models import Event, Occurrence
from temporale import utils, forms
from temporale.conf import settings as temporale_settings

@login_required
def events_as_vcal(request, events=None, **kwargs):
    """
    Return an iCal/vCal of all ``events``.

    If ``events`` is a queryset, clone it. If ``None``, default to all ``Event``s.

    Parameters:

    events
        an iterable of ``Event`` objects
    filename
        base filename for iCalendar, defaults to ``settings.PROJECT_NAME``.
    """
    if not events:
        events = Event.objects.all()
    elif hasattr(events, '_clone'):
        events = events._clone()
    if 'filename' in kwargs:
        filename = kwargs['filename']
    else:
        filename = settings.PROJECT_NAME

    cal = vobject.iCalendar()

    for e in events:
        for occ in e.occurrence_set.all():
            v = cal.add('vevent')
            v.add('dtstart').value = occ.start_time
            v.add('dtend').value = occ.end_time
            v.add('summary').value = e.title
            v.add('description').value = e.description
    response = HttpResponse(cal.serialize(), mimetype="text/calendar")
    response['Content-Disposition'] = 'attachment; filename=%s.ics' % filename
    return response
            