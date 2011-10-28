from django.db import models
from django.contrib.contenttypes import generic
from temporale.models import Event, create_event

class Person(models.Model):
    name = models.CharField(max_length=127)
    events = generic.GenericRelation(Event)

    def __unicode__(self):
        return self.name

    def add_event(self, **kwargs):
        """
        Add a single event to this person.
        
        Keyword arguments:
        
        :title: str/unicode
            default: ''
        :event_type: ``EventType`` or tuple(code,title)
            required
        :start_time: ``date`` or ``datetime``
            required
        :end_time: ``date`` or ``datetime``
            default: start_time
        :note: str/unicode
            text for sticky note (from ``fiee-adhesive``)
        :rrule_params:
            for multiple occurrences, see ``dateutil.rrule``
            default: only one occurrence
        """
        title = kwargs.pop('title', '')
        event_type = kwargs.pop('event_type')
        if not 'end_time' in kwargs:
            kwargs['end_time'] = kwargs['start_time']
        kwargs['content_object'] = self
        return create_event(title, event_type, **kwargs)
