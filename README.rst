==============
fiëé témporâle
==============

Generic event data for your Django models,
based on django-swingtime_ by David A. Krauth (dakrauth).

Use this to add arbitrary date-based relations to your models,
e.g. a person has a birthday, some life events and an obit;
a blog post has a creation date, a publishing date, an date of last edit and a revocation date;
a magazine issue has a publication day, editorial and advertising deadlines etc.

Or you might have a timetable of recurring courses, like in swingtime’s original demo app.

Using dateutil’s repetition rules, you can configure rather complicated occurrence patterns.

Finally show all your dates in a nice calendar or timeline view.


Differentiation
---------------

These generic events are good if you’d like to show very different events together in one calendar.

If you have very uniform event-based models, then this might be too complex for you.
I didn’t check yet, but I guess it hits the database rather hard.


Howto
-----

You don’t need to change your models at all, but you can add::

    events = django.contrib.contenttypes.field.GenericRelation(temporale.models.Event)


Otherwise you can define a `temporale_info` for your models like this::


    def temporale_info(self):
        """
        list of dicts about this model’s events to handle by temporale
        """
        res = [{
            'title': _(u'Publication date: %s') % self.name(),
            'event_type': ('pubday', _('Publication date')),
            'description': '',
            'start_time': self.pubday,
            'end_time': self.pubday,
            'user': self.lastchangedby,
            }]
        if self.revocationday:
            res.append({
            'title': _(u'Revocation: %s') % self.name(),
            'event_type': ('revocationday', _('Revocation date')),
            'description': '',
            'start_time': self.revocationday,
            'end_time': self.revocationday,
            'user': self.lastchangedby,
            })
        return res


fiëé temporâle listens to save events and handles all events that are defined this way.


Dependencies
------------

* Django 1.8 with included contributions
* django-registration_ (or compatible)
* fiee-dorsale_ 0.1.0+
* python-dateutil_ 1.5+ (not 2.0, that's only for Python 3!)


Known Issues
------------

* demo and tests are not yet updated to current code
* timeline view not started (planned with SIMILE widget)


Settings
--------


PROJECT_NAME :
    Set this to your main project name.
    
    Default: 'temporale'

You can influence the inheritance of temporale’s models and thus the
dependeny from other fiëé packages. Try to decide that first, because
different base models mean different model fields and thus different
database table columns.

TEMPORALE_BASE_CLASS : class name
    Default: `adhesive.models.DorsaleAnnotatedBaseModel` from fiee-adhesive_
    
    Other possibilities include `django.db.models.Model` and the models from
    fiee-dorsale_

TEMPORALE_MANAGER : class name
    Default: `dorsale.managers.DorsaleGroupSiteManager` from fiee-dorsale_
    
    Since this is called with arguments for group and site field names,
    you need a Manager class that accepts them. You can use
    `dorsale.managers.DorsaleFakeManager` or make your own.

TEMPORALE_USE_ADHESIVE : boolean
    Default: False
    
    If `True`, events try to save associated `adhesive.Notes`.


TEMPORALE_TIMESLOT_TIME_FORMAT : strftime string
    Default: '%H:%M'

    Used for formatting start and end time selectors in forms.

TEMPORALE_TIMESLOT_INTERVAL : `datetime.timedelta`
    Default: 15 minutes

    Used for creating start and end time form selectors as well as time slot
    grids.
    Value should be `datetime.timedelta` value representing the incremental 
    difference between temporal options

TEMPORALE_TIMESLOT_START_TIME : `datetime.time`
    Default: 09:00
    
    A `datetime.time` value indicting the starting time for time slot grids and
    form selectors

TEMPORALE_TIMESLOT_END_TIME_DURATION : `datetime.timedelta`
    Default: 8 hours
    
    A `datetime.timedelta` value indicating the offset value from 
    TEMPORALE_TIMESLOT_START_TIME for creating time slot grids and form
    selectors.
    Using a time delta makes it possible to span dates.
    For instance, one could have a starting time of 15:00 and wish to indicate 
    an ending value of 01:30, in which case a value of 
    `datetime.timedelta(hours=10.5)` could be specified to indicate that the
    01:30 represents the following date’s time and not the current date’s.

TEMPORALE_TIMESLOT_MIN_COLUMNS : int
    Default: 4
    
    Indicates a minimum value for the number grid columns to be shown in the
    time slot table.

TEMPORALE_DEFAULT_OCCURRENCE_DURATION : `datetime.timedelta`
    Default: 1 hour

    Indicate the default length in time for a new occurrence, specifed by using
    a `datetime.timedelta` object.

TEMPORALE_CALENDAR_FIRST_WEEKDAY : int
    Default: 1 (Monday)
    
    If not `None`, passed to the `calendar` module’s `setfirstweekday` function.

FIRST_DAY_OF_WEEK : int
    Same as TEMPORALE_CALENDAR_FIRST_WEEKDAY, inherits from the former.


License
-------

BSD, see LICENSE_
(may not entirely be allowed, must still check licenses of used code)


Author(s)
---------

* David A. Krauth (dakrauth)
* fiëé visuëlle, Henning Hraban Ramm, <hraban@fiee.net>, http://www.fiee.net
* contains code from the Django project and other sources (as indicated in the code)

.. _LICENSE: ./fiee-temporale/raw/master/LICENSE
.. _fiee-dorsale: https://github.com/fiee/fiee-dorsale
.. _django-swingtime: https://github.com/fiee/django-swingtime
.. _django-registration: https://bitbucket.org/ubernostrum/django-registration/
.. _python-dateutil: http://labix.org/python-dateutil
.. _YUI grids css: http://developer.yahoo.com/yui/grids/
.. _jQuery: http://docs.jquery.com/
.. _jQuery UI: http://jqueryui.com/demos/
