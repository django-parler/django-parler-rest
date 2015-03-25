# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from .models import Country
from .serializers import CountryTranslatedSerializer


class CountryTranslatedSerializerTestCase(TestCase):

    def setUp(self):
        self.country = Country.objects.create(
            country_code='ES', name="Spain",
            url="http://en.wikipedia.org/wiki/Spain"
        )
        self.country.set_current_language('es')
        self.country.name = "España"
        self.country.url = "http://es.wikipedia.org/wiki/Spain"
        self.country.save()

    def test_language_serialization(self):
        serializer = CountryTranslatedSerializer(self.country)
        self.assertEqual(serializer.data, {
            'pk': self.country.pk,
            'country_code': 'ES',
            'translations': {
                'en': {
                    'name': "Spain",
                    'url': "http://es.wikipedia.org/wiki/Spain"
                },
                'es': {
                    'name': "España",
                    'url': "http://es.wikipedia.org/wiki/España"
                }
            }
        })
