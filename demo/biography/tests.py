# -*- coding: utf-8 -*-
from datetime import datetime, date
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from demo.biography.models import Person
from temporale.models import *

#class BioViewsTest(TestCase):
#    def test_index(self):
#        resp = self.client.get('/bio/')
#        self.assertEqual(rest.status_code, 200)
#        # check resp.context!
#        
#    def test_missing(self):
#        resp = self.client('/something_nonexistant/')
#        self.assertEqual(rest.status_code, 404)
    
class BioEventsTest(TestCase):
    fixtures = ['biography_test.json',]
    
    def setUp(self):
        self.person_type = ContentType.objects.get_for_model(Person)
        self.luxemburg, self.curie, self.einstein = Person.objects.all()
        self.birthday, self.obit, self.lifespan = EventType.objects.all()
        
    def test_fixtures(self):
        self.assertEqual(EventType.objects.count(), 3)
        self.assertEqual(Person.objects.count(), 3)

    def test_single_events(self):
        # try direct event creation
        mc_b = Event(title='Birth', description='in Warszawa', event_type=self.birthday, content_object=self.luxemburg)
        mc_b.save()
        mc_b.add_single_occurrence(date(1867,11,7))

        self.assertEqual(Event.objects.count(), 1)
        
        mc_d = Event(title='Death', description='in Sancellemoz', event_type=self.obit, content_object=self.curie)
        mc_d.save()
        mc_d.add_single_occurrence(date(1934,7,4))
        self.assertEqual(Event.objects.count(), 2)
        
        # try create_event shortcut
        create_event('Birth', self.birthday, description=u'as Rozalia Luksenburg in Zamość', start_time=date(1871,3,5), content_object=self.luxemburg)
        self.assertEqual(Event.objects.count(), 3)

        create_event('Death', self.obit, description=u'murdered in Berlin', start_time=date(1919,1,15), content_object=self.luxemburg)
        self.assertEqual(Event.objects.count(), 4)
        
    def test_span_events(self):
        mc_l = Event(title='Life', description='', event_type=self.lifespan, content_object=self.curie)
        mc_l.save()
        mc_l.add_single_occurrence(date(1867,11,7), date(1934,7,4))
        
        create_event('Life', self.lifespan, description='', start_time=date(1871,3,5), end_time=date(1919,1,15), content_object=self.luxemburg)
        
        self.assertEqual(Event.objects.filter(event_type=self.lifespan).count(), 2)
        