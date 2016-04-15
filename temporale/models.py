# -*- coding: utf-8 *-*
from datetime import datetime, time
from django.utils.translation import ugettext as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.db.models.signals import post_save
# from dorsale.managers import DorsaleSiteManager
# from adhesive.models import DorsaleAnnotatedBaseModel
from dorsale.tools import class_from_name
from dateutil import rrule

import logging
logger = logging.getLogger(__name__)

from .settings import BASE_CLASS, MANAGER

BASE_CLASS = class_from_name(BASE_CLASS)
MANAGER = class_from_name(MANAGER)

logger.info(BASE_CLASS)
logger.info(MANAGER)

__all__ = (
    'EventType',
    'Event',
    'Occurrence',
    'create_event'
)


class EventType(models.Model):
    """
    Simple ``Event`` classification.
    """
    code = models.SlugField(_('code'), max_length=15, unique=True, help_text=_(u'Abbreviation of the label (internal use)'))
    label = models.CharField(_('label'), max_length=50, help_text=_(u'Visible name of the event type'))
    content_type = models.ForeignKey(ContentType, verbose_name=_('content type'), blank=True, null=True, help_text=_(u'This event type is valid for related objects of this type'))

    class Meta:
        verbose_name = _('event type')
        verbose_name_plural = _('event types')

    def __unicode__(self):
        return self.label


class Event(BASE_CLASS):
    """
    Container model for general metadata and associated ``Occurrence`` entries.
    """
    title = models.CharField(_('title'), max_length=63, help_text=_(u'Name of the event'))
    description = models.CharField(_('description'), max_length=255, help_text=_(u'Short description of the event'))
    event_type = models.ForeignKey(EventType, verbose_name=_('event type'), null=True, help_text=_(u'Type of the event'))

    content_type = models.ForeignKey(ContentType, verbose_name=_('content type'), blank=True, null=True, help_text=_(u'Type of the related object'))
    object_id = models.IntegerField(_('object id'), blank=True, null=True, help_text=_(u'ID of the related object'))
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('events')
        ordering = ('title', )
        permissions = [
            ('view_event', _(u'Can view event')),
        ]

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('temporale-event', [str(self.id)])

    def add_occurrences(self, start_time, end_time, **rrule_params):
        """
        Add one or more occurences to the event using a comparable API to
        ``dateutil.rrule``.

        If ``rrule_params`` does not contain a ``freq``, one will be defaulted
        to ``rrule.DAILY``.

        Because ``rrule.rrule`` returns an iterator that can essentially be
        unbounded, we need to slightly alter the expected behavior here in order
        to enforce a finite number of occurrence creation.

        If both ``count`` and ``until`` entries are missing from ``rrule_params``,
        only a single ``Occurrence`` instance will be created using the exact
        ``start_time`` and ``end_time`` values.
        """
        rrule_params.setdefault('freq', rrule.DAILY)

        if 'count' not in rrule_params and 'until' not in rrule_params:
            self.occurrence_set.create(start_time=start_time, end_time=end_time, createdby=self.createdby, site=self.site)
        else:
            delta = end_time - start_time
            for ev in rrule.rrule(dtstart=start_time, **rrule_params):
                self.occurrence_set.create(start_time=ev, end_time=ev + delta, createdby=self.createdby, site=self.site)

    def add_single_occurrence(self, start_time, end_time=None):
        """
        Add a single occurrence to the event, using ``start_time`` also as ``end_time`` if empty.
        """
        end_time = end_time or start_time
        self.occurrence_set.create(start_time=start_time, end_time=start_time, createdby=self.createdby, site=self.site)

    def upcoming_occurrences(self):
        """
        Return all occurrences that are set to start on or after the current
        time.
        """
        return self.occurrence_set.filter(start_time__gte=datetime.now())

    def next_occurrence(self):
        """
        Return the single occurrence set to start on or after the current time
        if available, otherwise ``None``.
        """
        upcoming = self.upcoming_occurrences()
        return upcoming and upcoming[0] or None

    def daily_occurrences(self, dt=None):
        """
        Convenience method wrapping ``Occurrence.objects.daily_occurrences``.
        """
        return Occurrence.objects.daily_occurrences(dt=dt, event=self)


class OccurrenceManager(MANAGER):
    use_for_related_fields = True

    def daily_occurrences(self, dt=None, event=None):
        """
        Returns a queryset of for instances that have any overlap with a
        particular day.

        * ``dt`` may be either a datetime.datetime, datetime.date object, or
          ``None``. If ``None``, default to the current day.

        * ``event`` can be an ``Event`` instance for further filtering.
        """
        dt = dt or datetime.now()
        start = datetime(dt.year, dt.month, dt.day)
        end = start.replace(hour=23, minute=59, second=59)
        qs = self.filter(
            models.Q(
                start_time__gte=start,
                start_time__lte=end,
            ) |
            models.Q(
                end_time__gte=start,
                end_time__lte=end,
            ) |
            models.Q(
                start_time__lt=start,
                end_time__gt=end
            )
        )

        return qs.filter(event=event) if event else qs


class Occurrence(BASE_CLASS):
    """
    Represents the start end time for a specific occurrence of a master ``Event``
    object.
    """
    start_time = models.DateTimeField(_('start time'), help_text=_(u'-'))
    end_time = models.DateTimeField(_('end time'), help_text=_(u'-'))
    event = models.ForeignKey(Event, verbose_name=_('event'), editable=False, help_text=_(u'-'))

    objects = OccurrenceManager()

    class Meta:
        verbose_name = _('occurrence')
        verbose_name_plural = _('occurrences')
        ordering = ('start_time', 'end_time')
        permissions = [
            ('view_occurrence', _(u'Can view occurrence')),
        ]

    def __unicode__(self):
        if self.end_time > self.start_time:
            return u'%s: %s – %s' % (self.title, self.start_time.isoformat(), self.end_time.isoformat())
        return u'%s: %s' % (self.title, self.start_time.isoformat())

    @models.permalink
    def get_absolute_url(self):
        return ('temporale-occurrence', [str(self.event.id), str(self.id)])

    def __cmp__(self, other):
        return cmp(self.start_time, other.start_time)

    @property
    def title(self):
        return self.event.title

    @property
    def description(self):
        return self.event.description

    @property
    def event_type(self):
        return self.event.event_type

    @property
    def content_type(self):
        return self.event.content_type

    @property
    def content_object(self):
        return self.event.content_object

    def wholeday(self):
        """
        Occurrence lasts the whole day?
        (time of ``start_time`` and ``end_time`` are both 00:00:00)
        """
        return (self.start_time.time() == time(0,0) == self.end_time.time())


def create_event(title, event_type, description='', start_time=None,
        end_time=None, note=None, content_object=None, **rrule_params):
    """
    Convenience function to create an ``Event``, optionally create an
    ``EventType``, and associated ``Occurrence``s. ``Occurrence`` creation
    rules match those for ``Event.add_occurrences``.

    Returns the newly created ``Event`` instance.

    Parameters

    ``event_type``
        can be either an ``EventType`` object or 2-tuple of ``(code,label)``,
        from which an ``EventType`` is either created or retrieved.

    ``start_time``
        will default to the current hour if ``None``

    ``end_time``
        will default to ``start_time`` plus temporale_settings.DEFAULT_OCCURRENCE_DURATION
        hour if ``None``

    ``note``
        some remark that you’d like to attach as a note (see `fiee-adhesive`)

    ``content_object``
        the object where you want to attach your new event

    ``freq``, ``count``, ``rrule_params``
        follow the ``dateutils`` API (see http://labix.org/python-dateutil)
    """
    from temporale.conf import settings as temporale_settings

    model_type = ContentType.objects.get_for_model(content_object)

    if isinstance(event_type, tuple):
        new_event_type, created = EventType.objects.get_or_create(
            code=event_type[0],
            content_type=model_type,
        )
        if created:
            new_event_type.label=event_type[1]
            new_event_type.save()
    else:
        new_event_type = event_type

    event = Event.objects.create(
        title=title,
        description=description,
        event_type=new_event_type,
        content_object=content_object,
    )
    if content_object:
        if hasattr(content_object, 'createdby'):
            event.createdby = content_object.createdby
        if hasattr(content_object, 'site'):
            event.site = content_object.site

    if note is not None:
        event.notes.create(note=note)

    start_time = start_time or datetime.now().replace(
        minute=0,
        second=0,
        microsecond=0
    )

    end_time = end_time or start_time + temporale_settings.DEFAULT_OCCURRENCE_DURATION
    event.add_occurrences(start_time, end_time, **rrule_params)
    return event


def update_event(sender, **kwargs):
    """
    A callback for every object saved to be able to update events accordingly.

    This function handles only models that provide a `temporale_info` method,
    returning a list/tuple of dicts with an entry for every "event" field of that model.

    Such a dict looks like
    {
    'title'          : self.title,     # unicode, required
    'event_type'     : ('generic', _(u'Generic event')), # EventType, default as shown
    'description'    : self.text,      # unicode, defaults to ''
    'start_time'     : self.starttime, # datetime, defaults to now
    'end_time'       : self.endtime,   # datetime, defaults to now
    'content_object' : self,           # object, defaults to the saved instance
    }
    """
    # params: sender = class, instance = object, created = True if new
    if not hasattr(sender, 'temporale_info'):
        return False
    instance = kwargs['instance']
    if hasattr(instance, 'temporale_ignore'):
        return False
    infos = instance.temporale_info()
    evts = None
    if not kwargs['created']: # model was saved before
        model_type = ContentType.objects.get_for_model(sender)
        evts = Event.objects.filter(content_type__pk=model_type.id, object_id=instance.id)
        evts.delete() # simply create anew - TODO! - that's mostly unnecessary
    #if not evts: # no events found (new model or not previously connected to temporale)
    for info in infos:
        i = {
             'title': '',
             'event_type': ('generic', _(u'Generic event')),
             'description': '',
             'start_time': datetime.now(),
             'end_time': datetime.now(),
             'content_object': instance,
        }
        i.update(info)
        create_event(
            i['title'],
            i['event_type'],
            description=i['description'],
            start_time=i['start_time'],
            end_time=i['end_time'],
            content_object=i['content_object'],
        )
#    else:
#        for ev in evts:
#            ocs = Occurrence.objects.filter(event=ev)
#            for oc in ocs:
#                # TODO: find the right info entry = i
#                oc.title=i['title']
#                oc.description=description=i['description']
#                oc.start_time=i['start_time']
#                oc.end_time=i['end_time']
#                oc.save()

post_save.connect(update_event)
