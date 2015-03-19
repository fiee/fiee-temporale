# -*- coding: utf-8 -*-
from django.contrib import admin
from dorsale.admin import DorsaleBaseAdmin
from temporale.models import EventType, Event, Occurrence


class OccurrenceInline(admin.TabularInline):
    model = Occurrence
    extra = 1


class EventTypeAdmin(DorsaleBaseAdmin):
    list_display = ['code', 'label', 'content_type']
    list_filter = ['content_type',]
    search_fields = ['code', 'label']


class EventAdmin(DorsaleBaseAdmin):
    list_select_related = True
    list_display = ['title', 'event_type', 'content_object', 'content_type',]
    list_filter = ['event_type', 'content_type',]
    inlines = (OccurrenceInline,)
    search_fields = ['title', 'description']


class OccurrenceAdmin(DorsaleBaseAdmin):
    list_select_related = True
    date_hierarchy = 'start_time'
    list_display = ['start_time', 'end_time', 'event_type', 'content_object',]
    # list_filter = ['event_type', 'content_type',]
    search_fields = ['event__title', 'event__description', 'event__event_type__label',]


admin.site.register(EventType, EventTypeAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Occurrence, OccurrenceAdmin)
