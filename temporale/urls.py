from django.conf.urls import url

urlpatterns = [
    url(r'^(?:calendar/)?$',
        'views.today_view',
        name='temporale-today'),

    url(r'^(?P<year>\d{4})/$',
        'views.year_view',
        name='temporale-yearly-view'),

    url(r'^(\d{4})/(0?[1-9]|1[012])/$',
        'views.month_view',
        name='temporale-monthly-view'),

    url(r'^(\d{4})/(0?[1-9]|1[012])/([0-3]?\d)/$',
        'views.day_view',
        name='temporale-daily-view'),

    url(r'^events/$',
        'views.event_listing',
        name='temporale-events'),

    url(r'^events/new/$',
        'views.add_event',
        name='temporale-add-event'),

    url(r'^events/add/$',
        'views.add_event'),

    url(r'^events/(\d+)/$',
        'views.event_view',
        name='temporale-event'),

    url(r'^events/(\d+)/(\d+)/$',
        'views.occurrence_view',
        name='temporale-occurrence'),

    url(r'^vcal/$',
        'vcal.events_as_vcal',
        name='temporale-vcal'),
]
