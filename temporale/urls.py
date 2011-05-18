from django.conf.urls.defaults import *

from temporale import views, vcal


urlpatterns = patterns('',
    url(r'^(?:calendar/)?$',
        view=views.today_view,
        name='temporale-today'),

    url(r'^(?P<year>\d{4})/$',
        view=views.year_view,
        name='temporale-yearly-view'),

    url(r'^(\d{4})/(0?[1-9]|1[012])/$',
        view=views.month_view,
        name='temporale-monthly-view'),

    url(r'^(\d{4})/(0?[1-9]|1[012])/([0-3]?\d)/$',
        view=views.day_view,
        name='temporale-daily-view'),

    url(r'^events/$',
        view=views.event_listing,
        name='temporale-events'),

    url(r'^events/new/$',
        view=views.add_event,
        name='temporale-add-event'),

    url(r'^events/add/$',
        view=views.add_event),

    url(r'^events/(\d+)/$',
        view=views.event_view,
        name='temporale-event'),

    url(r'^events/(\d+)/(\d+)/$',
        view=views.occurrence_view,
        name='temporale-occurrence'),

    url(r'^vcal/$',
        view=vcal.events_as_vcal,
        name='temporale-vcal'),
)
