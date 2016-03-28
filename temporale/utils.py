"""
Common features and functions for temporale
"""
from collections import defaultdict
from datetime import datetime, date, timedelta, time
import itertools

from django.db.models.query import QuerySet
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
#from dateutil import rrule
from temporale.conf import settings as temporale_settings
from temporale.models import Occurrence

from django.utils import timezone

from django.conf import settings
import logging
logger = logging.getLogger(settings.PROJECT_NAME)


def html_mark_safe(func):
    """
    Decorator for functions return strings that should be treated as template
    safe.
    """
    def decorator(*args, **kws):
        return mark_safe(func(*args, **kws))
    return decorator


def time_delta_total_seconds(time_delta):
    """
    Calculate the total number of seconds represented by a
    ``datetime.timedelta`` object
    """
    return time_delta.days * 3600 + time_delta.seconds


def month_boundaries(dt=None):
    """
    Return a 2-tuple containing the datetime instances for the first and last
    dates of the current month or using ``dt`` as a reference.
    """
    import calendar
    dt = dt or date.today()
    wkday, ndays = calendar.monthrange(dt.year, dt.month)
    start = datetime(dt.year, dt.month, 1)
    return (start, start + timedelta(ndays - 1))


def css_class_cycler():
    """
    Return a dictionary keyed by ``EventType`` code, 
    whose values are an iterable or cycle of CSS class names.
    """
    from temporale.models import EventType
    return defaultdict(
        lambda: itertools.cycle(('evt-even', 'evt-odd')).next,
        ((e.code, itertools.cycle((
             'evt-%s-even' % e.code,
             'evt-%s-odd' % e.code
             )).next) for e in EventType.objects.all()
        )
    )


class BaseOccurrenceProxy(object):
    """
    A simple wrapper class for handling the presentational aspects of an
    ``Occurrence`` instance.
    """
    def __init__(self, occurrence, col):
        self.column = col
        self._occurrence = occurrence
        self.event_class = ''

    def __getattr__(self, name):
        return getattr(self._occurrence, name)

    def __unicode__(self):
        return self.title


class DefaultOccurrenceProxy(BaseOccurrenceProxy):

    def __init__(self, *args, **kws):
        super(DefaultOccurrenceProxy, self).__init__(*args, **kws)
        link = '<a href="%s">%s</a>' % (
            self.get_absolute_url(),
            self.title
        )

        self._str = itertools.chain((link,),itertools.repeat('&darr;')).next

    @html_mark_safe
    def __unicode__(self):
        logger.debug(self.title)
        return self._str()


def create_timeslot_table(dt=None, items=None,
    start_time=temporale_settings.TIMESLOT_START_TIME,
    end_time_delta=temporale_settings.TIMESLOT_END_TIME_DURATION,
    time_delta=temporale_settings.TIMESLOT_INTERVAL,
    min_columns=temporale_settings.TIMESLOT_MIN_COLUMNS,
    css_class_cycles=css_class_cycler,
    proxy_class=DefaultOccurrenceProxy):
    """
    Create a grid-like object representing a sequence of times (rows) and
    columns where cells are either empty or reference a wrapper object for
    event occasions that overlap a specific time slot.

    Currently, there is an assumption that if an occurrence has a ``start_time``
    that falls within the temporal scope of the grid, then that ``start_time`` will
    also match an interval in the sequence of the computed row entries.

    * ``dt`` - a ``datetime.datetime`` instance or ``None`` to default to now
    * ``items`` - a queryset or sequence of ``Occurrence`` instances. If
      ``None``, default to the daily occurrences for ``dt``.
    * ``start_time`` - a ``datetime.time`` instance
    * ``end_time_delta`` - a ``datetime.timedelta`` instance
    * ``time_delta`` - a ``datetime.timedelta`` instance
    * ``min_column`` - the minimum number of columns to show in the table
    * ``css_class_cycles`` - if not ``None``, a callable returning a dictionary
      keyed by desired ``EventType`` abbreviations with values that iterate over
      progressive CSS class names for the particular abbreviation.
    * ``proxy_class`` - a wrapper class for accessing an ``Occurrence`` object.
      This class should also expose ``event_type`` and ``event_type`` attrs, and
      handle the custom output via its __unicode__ method.
    """
    dt = dt or datetime.now()
    dt0 = datetime.combine(dt.date(), time(0,0))
    dtstart = datetime.combine(dt.date(), start_time)
    dtend = dtstart + end_time_delta
    wholedaytime = datetime.combine(dt.date(), time(0,0,1))

    logger.info("new table from %s %s to %s", dt.date(), start_time, dtend.time())

    if isinstance(items, QuerySet):
        items = items._clone()
    elif not items:
        items = Occurrence.objects.daily_occurrences(dt).select_related('event')

    # build a mapping of timeslot "buckets"
    timeslots = { wholedaytime : {}, }
    n = dtstart
    while n <= dtend:
        timeslots[n] = {}
        n += time_delta

    # fill the timeslot buckets with occurrence proxies
    for item in sorted(items):
        if item.end_time < dt0 or item.start_time > dtend \
        or (item.end_time <= dtstart and not item.wholeday()): # wholeday is normally < start time
            # events outside of our schedule constraints
            logger.debug("excluding %s", item)
            continue
        
        if item.wholeday():
            # whole day events
            rowkey = current = wholedaytime
        elif item.start_time > dtstart:
            # event started after our start time
            rowkey = current = item.start_time
        else:
            # event started on/before our start time
            rowkey = current = dtstart

        timeslot = timeslots.get(rowkey, None)
        if timeslot is None:
            logger.warn("timeslot not found for %s", item)
            # TODO fix atypical interval boundry spans
            # This is rather draconian, we should probably try to find a better
            # way to indicate that this item actually occurred between 2 intervals
            # and to account for the fact that this item may be spanning cells
            # but on weird intervals
            continue

        colkey = 0
        while 1:
            # keep searching for an open column to place this occurrence
            if colkey not in timeslot:
                proxy = proxy_class(item, colkey)
                timeslot[colkey] = proxy
                
                if item.wholeday():
                    break

                while current < item.end_time:
                    rowkey = current
                    row = timeslots.get(rowkey, None)
                    if row is None:
                        break

                    # we might want to put a sanity check in here to ensure that
                    # we aren't trampling some other entry, but by virtue of
                    # sorting all occurrence that shouldn't happen
                    row[colkey] = proxy
                    current += time_delta
                break

            colkey += 1

    # determine the number of timeslot columns we should show
    column_lens = [len(x) for x in timeslots.itervalues()]
    column_count = max((min_columns, max(column_lens) if column_lens else 0))
    column_range = range(column_count)
    empty_columns = ['' for x in column_range]

    if css_class_cycles:
        column_classes = dict([(i, css_class_cycles()) for i in column_range])
    else:
        column_classes = None

    # create the chronological grid layout
    table = []
    for rowkey in sorted(timeslots.keys()):
        cols = empty_columns[:]
        for colkey in timeslots[rowkey]:
            proxy = timeslots[rowkey][colkey]
            cols[colkey] = proxy
            if not proxy.event_class and column_classes and proxy.event_type:
                proxy.event_class = column_classes[colkey][proxy.event_type.code]()
        if rowkey == wholedaytime:
            rowkey = _(u'whole day')
        else:
            rowkey = rowkey.strftime('%H:%M')
        table.append((rowkey, cols))

    return table
