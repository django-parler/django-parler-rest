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

    def test_translations_serialization(self):
        expected = {
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
                },
            }
        }
        serializer = CountryTranslatedSerializer(self.country)
        self.assertItemsEqual(serializer.data, expected)

    def test_translations_validation(self):
        data = {
            'country_code': 'FR',
            'translations': {
                'en': {
                    'name': "France",
                    'url': "http://en.wikipedia.org/wiki/France"
                },
                'es': {
                    'name': "Francia",
                    'url': "http://es.wikipedia.org/wiki/Francia"
                },
            }
        }
        serializer = CountryTranslatedSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertItemsEqual(serializer.validated_data['translations'], data['translations'])

    def test_translated_fields_validation(self):
        data = {
            'country_code': 'FR',
            'translations': {
                'en': {
                    'url': "http://en.wikipedia.org/wiki/France"
                },
                'es': {
                    'url': "http://es.wikipedia.org/wiki/Francia"
                },
            }
        }
        serializer = CountryTranslatedSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('translations', serializer.errors)
        self.assertItemsEqual(serializer.errors['translations'], ('en', 'es'))
        self.assertIn('name', serializer.errors['translations']['en'])
        self.assertIn('name', serializer.errors['translations']['es'])

    def test_tranlations_saving(self):
        data = {
            'country_code': 'FR',
            'translations': {
                'en': {
                    'name': "France",
                    'url': "http://en.wikipedia.org/wiki/France"
                },
                'es': {
                    'name': "Francia",
                    'url': "http://es.wikipedia.org/wiki/Francia"
                },
            }
        }
        serializer = CountryTranslatedSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        instance = serializer.save()
        instance = Country.objects.get(pk=instance.pk)
        instance.set_current_language('en')
        self.assertEqual(instance.name, "France")
        self.assertEqual(instance.url, "http://en.wikipedia.org/wiki/France")
        instance.set_current_language('es')
        self.assertEqual(instance.name, "Francia")
        self.assertEqual(instance.url, "http://es.wikipedia.org/wiki/Francia")
