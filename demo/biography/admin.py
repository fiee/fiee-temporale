# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.contenttypes import generic
from dorsale.admin import DorsaleBaseAdmin
from temporale.models import EventType, Event, Occurrence
from biography.models import Person

class EventInline(generic.GenericTabularInline):
    model = Event
    extra = 2

class PersonAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    inlines = (EventInline,)

admin.site.register(Person, PersonAdmin)
