#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from subprocess import check_call, CalledProcessError

PROJECT_NAME = getattr(settings, 'PROJECT_NAME', 'temporale')

# base manager for temporale Models
MANAGER = getattr(settings, 'TEMPORALE_MANAGER', 'dorsale.managers.DorsaleSiteManager')

# parent class of temporale Models (descendand of django.models.Model)
BASE_CLASS = getattr(settings, 'TEMPORALE_BASE_CLASS', 'adhesive.models.DorsaleAnnotatedBaseModel')

# expect adhesive notes in event forms?
USE_ADHESIVE = getattr(settings, 'TEMPORALE_USE_ADHESIVE', False)


# A "strftime" string for formatting start and end time selectors in forms
TIMESLOT_TIME_FORMAT = getattr(settings, 'TEMPORALE_TIMESLOT_TIME_FORMAT', '%H:%M')

# Used for creating start and end time form selectors as well as time slot grids.
# Value should be datetime.timedelta value representing the incremental 
# differences between temporal options
TIMESLOT_INTERVAL = getattr(settings, 'TEMPORALE_TIMESLOT_INTERVAL', datetime.timedelta(minutes=15))

# A datetime.time value indicting the starting time for time slot grids and form
# selectors
TIMESLOT_START_TIME = getattr(settings, 'TEMPORALE_TIMESLOT_START_TIME', datetime.time(9))

# A datetime.timedelta value indicating the offset value from 
# TIMESLOT_START_TIME for creating time slot grids and form selectors. The for
# using a time delta is that it possible to span dates. For instance, one could
# have a starting time of 3pm (15:00) and wish to indicate a ending value 
# 1:30am (01:30), in which case a value of datetime.timedelta(hours=10.5) 
# could be specified to indicate that the 1:30 represents the following date's
# time and not the current date.
TIMESLOT_END_TIME_DURATION = getattr(settings, 'TEMPORALE_TIMESLOT_END_TIME_DURATION', datetime.timedelta(hours=+8))

# Indicates a minimum value for the number grid columns to be shown in the time
# slot table.
TIMESLOT_MIN_COLUMNS = getattr(settings, 'TEMPORALE_TIMESLOT_MIN_COLUMNS', 4)

# Indicate the default length in time for a new occurrence, specifed by using
# a datetime.timedelta object
DEFAULT_OCCURRENCE_DURATION = getattr(settings, 'TEMPORALE_DEFAULT_OCCURRENCE_DURATION', datetime.timedelta(hours=+1))

# If not None, passed to the calendar module's setfirstweekday function.
# also FIRST_DAY_OF_WEEK
CALENDAR_FIRST_WEEKDAY = getattr(settings, 'TEMPORALE_CALENDAR_FIRST_WEEKDAY', 1)
FIRST_DAY_OF_WEEK = getattr(settings, 'FIRST_DAY_OF_WEEK', CALENDAR_FIRST_WEEKDAY)
