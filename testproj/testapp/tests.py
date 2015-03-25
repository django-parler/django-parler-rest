# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

import six

from .models import Country
from .serializers import CountryTranslatedSerializer


class CountryTranslatedSerializerTestCase(TestCase):

    def setUp(self):
        self.instance = Country.objects.create(
            country_code='ES', name="Spain",
            url="http://en.wikipedia.org/wiki/Spain"
        )
        self.instance.set_current_language('es')
        self.instance.name = "España"
        self.instance.url = "http://es.wikipedia.org/wiki/Spain"
        self.instance.save()

    def test_translations_serialization(self):
        expected = {
            'pk': self.instance.pk,
            'country_code': 'ES',
            'translations': {
                'en': {
                    'name': "Spain",
                    'url': "http://en.wikipedia.org/wiki/Spain"
                },
                'es': {
                    'name': "España",
                    'url': "http://es.wikipedia.org/wiki/España"
                },
            }
        }
        serializer = CountryTranslatedSerializer(self.instance)
        six.assertCountEqual(self, serializer.data, expected)

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
        six.assertCountEqual(self, serializer.validated_data['translations'], data['translations'])

    def test_translated_fields_validation(self):
        data = {
            'country_code': 'FR',
            'translations': {
                'en': {
                    'url': "http://en.wikipedia.org/wiki/France"
                },
                'es': {
                    'name': "Francia",
                    'url': "es.wikipedia.org/wiki/Francia"
                },
            }
        }
        serializer = CountryTranslatedSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('translations', serializer.errors)
        six.assertCountEqual(self, serializer.errors['translations'], ('en', 'es'))
        self.assertIn('name', serializer.errors['translations']['en'])
        self.assertIn('url', serializer.errors['translations']['es'])

    def test_tranlations_saving_on_create(self):
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

    def test_translations_saving_on_update(self):
        data = {
            'country_code': 'ES',
            'translations': {
                'en': {
                    'name': "Spain",
                    'url': "http://en.wikipedia.org/wiki/Spain"
                },
                'es': {
                    'name': "Hispania",
                    'url': "http://es.wikipedia.org/wiki/Hispania"
                },
                'fr': {
                    'name': "Espagne",
                    'url': "http://fr.wikipedia.org/wiki/Espagne"
                }
            }
        }
        serializer = CountryTranslatedSerializer(self.instance, data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        instance = serializer.save()
        instance = Country.objects.get(pk=instance.pk)
        instance.set_current_language('en')
        self.assertEqual(instance.name, "Spain")
        self.assertEqual(instance.url, "http://en.wikipedia.org/wiki/Spain")
        instance.set_current_language('es')
        self.assertEqual(instance.name, "Hispania")
        self.assertEqual(instance.url, "http://es.wikipedia.org/wiki/Hispania")
        instance.set_current_language('fr')
        self.assertEqual(instance.name, "Espagne")
        self.assertEqual(instance.url, "http://fr.wikipedia.org/wiki/Espagne")
