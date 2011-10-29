#!/usr/bin/env python
from pprint import pprint, pformat
from cStringIO import StringIO
from datetime import datetime, timedelta, date, time

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.management import call_command

from temporale import utils
from temporale.models import *

expected_table_0 = """\
| whole day | holy     |          |          |          |          |
"""

expected_table_1 = expected_table_0 + """\
| 15:00 | gamma    |          |          |          |          |
| 15:15 | zelda    |          |          |          |          |
| 15:30 | zelda    | alpha    |          |          |          |
| 15:45 |          | alpha    |          |          |          |
| 16:00 | bravo    | alpha    | foxtrot  |          |          |
| 16:15 | bravo    | alpha    | foxtrot  | charlie  |          |
| 16:30 | bravo    | alpha    | foxtrot  | charlie  | delta    |
| 16:45 |          | alpha    |          | charlie  | delta    |
| 17:00 |          | alpha    |          |          | delta    |
| 17:15 | echo     | alpha    |          |          |          |
| 17:30 | echo     | alpha    |          |          |          |
| 17:45 | echo     |          |          |          |          |
| 18:00 | gamma    |          |          |          |          |
"""

expected_table_2 = expected_table_0 + """\
| 15:30 | zelda    | alpha    |          |          |          |
| 15:45 |          | alpha    |          |          |          |
| 16:00 | bravo    | alpha    | foxtrot  |          |          |
| 16:15 | bravo    | alpha    | foxtrot  | charlie  |          |
| 16:30 | bravo    | alpha    | foxtrot  | charlie  | delta    |
| 16:45 |          | alpha    |          | charlie  | delta    |
| 17:00 |          | alpha    |          |          | delta    |
| 17:15 | echo     | alpha    |          |          |          |
| 17:30 | echo     | alpha    |          |          |          |
"""

expected_table_3 = expected_table_0 + """\
| 16:00 | alpha    | bravo    | foxtrot  |          |          |
| 16:15 | alpha    | bravo    | foxtrot  | charlie  |          |
| 16:30 | alpha    | bravo    | foxtrot  | charlie  | delta    |
| 16:45 | alpha    |          |          | charlie  | delta    |
| 17:00 | alpha    |          |          |          | delta    |
| 17:15 | alpha    | echo     |          |          |          |
| 17:30 | alpha    | echo     |          |          |          |
"""

expected_table_4 = """\
| whole day | holy     |          |          |          |
| 18:00 | gamma    |          |          |          |
| 18:15 | gamma    |          |          |          |
| 18:30 | gamma    |          |          |          |
| 18:45 | gamma    |          |          |          |
| 19:00 | gamma    |          |          |          |
| 19:15 | gamma    |          |          |          |
| 19:30 | gamma    |          |          |          |
"""

expected_table_5 = expected_table_0 + """\
| 16:30 | alpha    | bravo    | foxtrot  | charlie  | delta    |
"""


class TableTest(TestCase):
    fixtures = ['temporale_test']

    def setUp(self):
        self._dt = datetime(2011,12,11)

    def table_as_string(self, table):
        timefmt = '| %-5s'
        cellfmt = '| %-8s'
        out = StringIO()
        for tm, cells in table:
            print >> out, timefmt % tm,
            for cell in cells:
                if cell:
                    print >> out, cellfmt % cell.event.title,
                else:
                    print >> out, cellfmt % '',
            print >> out, '|'

        return out.getvalue()

    def _do_test(self, start, end, expect):
        #import pdb
        start = time(*start)
        dtstart = datetime.combine(self._dt, start)
        etd = datetime.combine(self._dt, time(*end)) - dtstart

        # pdb.set_trace()
        table = utils.create_timeslot_table(self._dt, start_time=start, end_time_delta=etd)

        actual = self.table_as_string(table)
        out = '\nExpecting:\n%s\nActual:\n%s' % (expect, actual)
        #print out
        self.assertEqual(actual, expect, out)

    def test_slot_table_1(self):
        self._do_test((15,0), (18,0), expected_table_1)

    def test_slot_table_2(self):
        self._do_test((15,30), (17,30), expected_table_2)

    def test_slot_table_3(self):
        self._do_test((16,0), (17,30), expected_table_3)

    def test_slot_table_4(self):
        self._do_test((18,0), (19,30), expected_table_4)

    def test_slot_table_5(self):
        self._do_test((16,30), (16,30), expected_table_5)


class NewEventFormTest(TestCase):
    fixtures = ['temporale_test']

    def test_new_event_simple(self):
        from temporale.forms import EventForm, MultipleOccurrenceForm
        et = EventType.objects.create(code='test', label='Test')

        data = dict(
            title='QWERTY',
            event_type=1,
            day='2011-12-11',
            start_time_delta='28800',
            end_time_delta='29700',
            year_month_ordinal_day='2',
            month_ordinal_day='2',
            holidays='skip',
            year_month_ordinal='1',
            month_option='each',
            repeats='count',
            freq='2',
            occurences='2',
            month_ordinal='1'
        )

        evt_form = EventForm(data)
        occ_form = MultipleOccurrenceForm(data)
        self.assertTrue(evt_form.is_valid(), evt_form.errors.as_text())
        self.assertTrue(occ_form.is_valid(), occ_form.errors.as_text())

        self.assertEqual(
            occ_form.cleaned_data['start_time'],
            datetime(2011, 12, 11, 8),
            'Bad start_time: %s' % pformat(occ_form.cleaned_data)
        )

def doc_tests():
    fixtures = ['temporale_test']
    """
        >>> from dateutil import rrule
        >>> from datetime import datetime
        >>> from temporale.models import *
        >>> evt_types = [EventType.objects.create(code=l.lower(),label=l) for l in ['Foo', 'Bar', 'Baz']]
        >>> evt_types
        [<EventType: Foo>, <EventType: Bar>, <EventType: Baz>]
        >>> e = Event.objects.create(title='Hello, world', description='Happy New Year', event_type=evt_types[0])
        >>> e
        <Event: Hello, world>
        >>> e.add_occurrences(datetime(2011,1,1), datetime(2011,1,1,1), freq=rrule.YEARLY, count=7)
        >>> e.occurrence_set.all()
        [<Occurrence: Hello, world: 2011-01-01T00:00:00>, <Occurrence: Hello, world: 2009-01-01T00:00:00>, <Occurrence: Hello, world: 2010-01-01T00:00:00>, <Occurrence: Hello, world: 2011-01-01T00:00:00>, <Occurrence: Hello, world: 2012-01-01T00:00:00>, <Occurrence: Hello, world: 2013-01-01T00:00:00>, <Occurrence: Hello, world: 2014-01-01T00:00:00>]
        >>> e = create_event('Bicycle repairman', evt_types[2], content_object=evt_types[0])
        >>> e.occurrence_set.count()
        1
        >>> e = create_event(
        ...     'Something completely different',
        ...     ('abbr', 'Abbreviation'),
        ...     start_time=datetime(2011,12,1, 12),
        ...     content_object=evt_types[0],
        ...     freq=rrule.WEEKLY,
        ...     byweekday=(rrule.TU, rrule.TH),
        ...     until=datetime(2011,12,31)
        ... )
        >>> for o in e.occurrence_set.all():
        ...     print o.start_time, o.end_time
        ...
        2011-12-02 12:00:00 2011-12-02 13:00:00
        2011-12-04 12:00:00 2011-12-04 13:00:00
        2011-12-09 12:00:00 2011-12-09 13:00:00
        2011-12-11 12:00:00 2011-12-11 13:00:00
        2011-12-16 12:00:00 2011-12-16 13:00:00
        2011-12-18 12:00:00 2011-12-18 13:00:00
        2011-12-23 12:00:00 2011-12-23 13:00:00
        2011-12-25 12:00:00 2011-12-25 13:00:00
        2011-12-30 12:00:00 2011-12-30 13:00:00
    """
    pass