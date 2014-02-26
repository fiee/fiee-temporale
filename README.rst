==============
fiëé témporâle
==============

Generic event data for your Django models,
based on django-swingtime_ by David A. Krauth (dakrauth)
(at the moment it’s mostly his code, that will probably change).

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

You don’t need to change your models at all, but it’s easier if you add::

    events = django.contrib.contenttypes.generic.GenericRelation(temporale.models.Event)


Dependencies
------------

* Django 1.6 with included contributions
* django-registration_ (or compatible)
* fiee-dorsale_
* python-dateutil_ 1.5+ (not 2.0 or above, that's only for Python 3!)


Known Issues
------------

* fork of my personal version of swingtime, not yet working at all
* timeline view not started (planned with SIMILE widget)


License
-------

BSD, like Django itself, see LICENSE_
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
