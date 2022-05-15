"""Serializer integration tests."""

import unittest

from django.test import TestCase

from parler.tests.utils import override_parler_settings

from parler_rest.utils import create_translated_fields_serializer

from .models import Country, Picture
from .serializers import (
    CountryTranslatedSerializer,
    CountryAutoSharedModelTranslatedSerializer,
    CountryExplicitTranslatedSerializer,
    ContinentCountriesTranslatedSerializer,
    PictureCaptionSerializer, FlatContinentCountriesTranslatedSerializer, FlatCountryTranslatedSerializer,
    FlatCountryNoLanguageCodeTranslatedSerializer, FlatCountryExplicitLangTranslatedSerializer,
)


class CountryTranslatedSerializerTestCase(TestCase):

    # Disable cache as due to automatic db rollback the instance pk
    # is the same for all tests and with the cache we'd mistakenly
    # skips saves after the first test.
    @override_parler_settings(PARLER_ENABLE_CACHING=False)
    def setUp(self):
        self.instance = Country.objects.create(
            country_code='ES', name="Spain",
            url="http://en.wikipedia.org/wiki/Spain"
        )
        self.instance.set_current_language('es')
        self.instance.name = "España"
        self.instance.url = "http://es.wikipedia.org/wiki/España"
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
        self.assertCountEqual(serializer.data, expected)

    def test_translations_serialization_only_some_languages(self):
        self.instance.set_current_language('fr')
        self.instance.name = "Espagne"
        self.instance.url = "https://fr.wikipedia.org/wiki/Espagne"
        self.instance.save_translations()
        # So we got: en, es, fr: Let's drop the english
        expected = {
            'pk': self.instance.pk,
            'country_code': 'ES',
            'translations': {
                'es': {
                    'name': "Spain",
                    'url': "http://en.wikipedia.org/wiki/Spain"
                },
                'fr': {
                    'name': "Espagne",
                    'url': "https://fr.wikipedia.org/wiki/Espagne"
                },
            }
        }
        context = {'languages': ['es', 'fr']}
        serializer = CountryTranslatedSerializer(self.instance, context=context)
        self.assertCountEqual(serializer.data, expected)

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
        self.assertCountEqual(serializer.validated_data['translations'], data['translations'])

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
        self.assertCountEqual(serializer.errors['translations'], ('en', 'es'))
        self.assertIn('name', serializer.errors['translations']['en'])
        self.assertIn('url', serializer.errors['translations']['es'])

    def test_translations_validation_empty(self):
        for empty_value in (None, {}, '', ):
            data = {
                'country_code': 'FR',
                'translations': empty_value
            }
            serializer = CountryTranslatedSerializer(data=data)
            self.assertFalse(serializer.is_valid())
            self.assertIn('translations', serializer.errors)

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

    def test_deserialization_invalid_data_types(self):
        data = {"translations": "this is not a dict"}
        serializer = CountryTranslatedSerializer(self.instance, data=data, partial=True)
        assert not serializer.is_valid()

    def test_automatically_deduced_shared_model(self):
        serializer = CountryAutoSharedModelTranslatedSerializer(self.instance)
        assert serializer.data["translations"]

    def test_explicitly_declared_translation_field_serializer(self):
        serializer = CountryExplicitTranslatedSerializer(self.instance)
        translations = serializer.data["trans"]
        assert translations["en"]["name"] == "Spain"
        assert "url" not in translations["en"]
        assert translations["es"]["name"] == "España"
        assert "url" not in translations["es"]

        # Test update:
        data = {
            "trans": {
                "fi": {
                    "name": "Espanja"
                }
            }
        }
        serializer = CountryExplicitTranslatedSerializer(self.instance, data=data, partial=True)
        assert serializer.is_valid()
        instance = serializer.save()
        instance.set_current_language("en")
        assert instance.name == "Spain"
        instance.set_current_language("fi")
        assert instance.name == "Espanja"

    def test_nested_translated_serializer(self):
        data = {
            "continent": "Europe",
            "countries": [{
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
            }]
        }
        serializer = ContinentCountriesTranslatedSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        nested_data = serializer.validated_data['countries'][0]
        expected = data['countries'][0]
        self.assertCountEqual(nested_data, expected)


class ParlerRestUtilsTestCase(unittest.TestCase):

    def test_automatic_translation_serializer_creation(self):
        serializer = create_translated_fields_serializer(Country)()
        assert serializer.fields["name"]
        assert serializer.fields["url"]
        assert serializer.fields["language_code"]


class PictureCaptionSerializerTestCase(TestCase):

    # Disable cache as due to automatic db rollback the instance pk
    # is the same for all tests and with the cache we'd mistakenly
    # skips saves after the first test.
    @override_parler_settings(PARLER_ENABLE_CACHING=False)
    def setUp(self):
        self.instance = Picture.objects.create(
            image_nr=1,
            caption="Spain",
        )
        self.instance.set_current_language('es')
        self.instance.caption = "España"
        self.instance.save()

    def test_translation_serialization(self):
        expected = {
            'image_nr': self.instance.image_nr,
            'caption': {
                'en': "Spain",
                'es': "España",
            }
        }
        serializer = PictureCaptionSerializer(self.instance)
        self.assertCountEqual(serializer.data, expected)

    def test_translation_deserialization(self):
        data = {
            'image_nr': 2,
            'caption': {
                'en': "Spain",
                'de': "Spanien",
            }
        }
        serializer = PictureCaptionSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        instance = serializer.save()
        self.assertIsInstance(instance, Picture)
        self.assertEqual(instance.get_current_language(), 'en')
        self.assertEqual(instance.image_nr, 2)
        self.assertEqual(instance.caption, "Spain")
        instance.set_current_language('de')
        self.assertEqual(instance.caption, "Spanien")
        instance.set_current_language('es')
        self.assertEqual(instance.caption, "Spain")  # fallback on default


class FlatCountryTranslatedSerializerTestCase(TestCase):
    # Disable cache as due to automatic db rollback the instance pk
    # is the same for all tests and with the cache we'd mistakenly
    # skips saves after the first test.
    @override_parler_settings(PARLER_ENABLE_CACHING=False)
    def setUp(self):
        self.instance = Country.objects.create(
            country_code='ES', name="Spain",
            url="http://en.wikipedia.org/wiki/Spain"
        )
        self.instance.set_current_language('es')
        self.instance.name = "España"
        self.instance.url = "http://es.wikipedia.org/wiki/España"
        self.instance.save()

    def test_en_translations_serialization(self):
        self.instance.set_current_language('en')
        expected_en = {
            'pk': self.instance.pk,
            'country_code': 'ES',
            'language_code': 'en',
            'name': "Spain",
            'url': "http://en.wikipedia.org/wiki/Spain"
        }
        serializer = FlatCountryTranslatedSerializer(self.instance)
        self.assertDictEqual(serializer.data, expected_en)

    def test_es_translations_serialization(self):
        self.instance.set_current_language('es')
        expected_es = {
            'pk': self.instance.pk,
            'country_code': 'ES',
            'language_code': 'es',
            'name': "España",
            'url': "http://es.wikipedia.org/wiki/España"
        }
        serializer = FlatCountryTranslatedSerializer(self.instance)
        self.assertDictEqual(serializer.data, expected_es)

    def test_translations_serialization_no_language_code(self):
        self.instance.set_current_language('es')
        serializer = FlatCountryNoLanguageCodeTranslatedSerializer(self.instance)
        expected = {
            'pk': self.instance.pk,
            'country_code': 'ES',
            'name': "España",
            'url': "http://es.wikipedia.org/wiki/España"
        }
        self.assertDictEqual(serializer.data, expected)

    def test_language_code_validation(self):
        data = {
            'country_code': 'es',
            'language_code': 'es',
            'name': 'España',
            'url': "http://es.wikipedia.org/wiki/España"
        }
        serializer = FlatCountryTranslatedSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_language_code_invalid(self):
        data = {
            'country_code': 'es',
            'language_code': 'fr',
            'name': 'Espagne',
            'url': "http://fr.wikipedia.org/wiki/Espagne"
        }
        serializer = FlatCountryTranslatedSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('language_code', serializer.errors)
        self.assertEqual(serializer.errors['language_code'][0], '"fr" is not a valid choice.')

    def test_translated_fields_validation(self):
        data = {
            'country_code': 'FR',
            'language_code': 'en',
            'url': "es.wikipedia.org/wiki/Francia"
        }
        serializer = FlatCountryTranslatedSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
        self.assertEqual(serializer.errors['name'][0], 'This field is required.')
        self.assertIn('url', serializer.errors)
        self.assertEqual(serializer.errors['url'][0], 'Enter a valid URL.')

    def test_translation_saving_on_create(self):
        data = {
            'country_code': 'FR',
            'language_code': 'es',
            'name': "Francia",
            'url': "http://es.wikipedia.org/wiki/Francia"
        }
        serializer = FlatCountryTranslatedSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        instance = serializer.save()
        instance = Country.objects.get(pk=instance.pk)
        instance.set_current_language('es')
        self.assertEqual(instance.name, "Francia")
        self.assertEqual(instance.url, "http://es.wikipedia.org/wiki/Francia")

    def test_translation_saving_on_update(self):
        data = {
            'country_code': 'E',
            'language_code': 'es',
            'name': "Hispania",
            'url': "http://es.wikipedia.org/wiki/Hispania"
        }
        serializer = FlatCountryTranslatedSerializer(self.instance, data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        instance = serializer.save()
        instance = Country.objects.get(pk=instance.pk)
        self.assertEqual(instance.country_code, 'E')  # also check if shared model is updated

        instance.set_current_language('es')
        self.assertEqual(instance.name, "Hispania")
        self.assertEqual(instance.url, "http://es.wikipedia.org/wiki/Hispania")

    def test_translations_saving_on_update_with_new_translation(self):
        data = {
            'country_code': 'ES',
            'language_code': 'fr',
            'name': "Espagne",
            'url': "http://fr.wikipedia.org/wiki/Espagne"
        }
        # Language choices are automatically verified against settings,
        # thus using a serializer with explicitly set language choices
        serializer = FlatCountryExplicitLangTranslatedSerializer(self.instance, data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        instance = serializer.save()
        instance = Country.objects.get(pk=instance.pk)
        instance.set_current_language('fr')
        self.assertEqual(instance.name, "Espagne")
        self.assertEqual(instance.url, "http://fr.wikipedia.org/wiki/Espagne")

    def test_translation_saving_on_create_no_language_code(self):
        data = {
            'country_code': 'FR',
            'name': "French",
            'url': "http://en.wikipedia.org/wiki/French"
        }
        serializer = FlatCountryNoLanguageCodeTranslatedSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        instance = serializer.save()
        instance = Country.objects.get(pk=instance.pk)
        instance.set_current_language('en')  # The fallback language, set via get_language
        self.assertEqual(instance.name, "French")
        self.assertEqual(instance.url, "http://en.wikipedia.org/wiki/French")

    def test_nested__translatedserializer(self):
        data = {
            "continent": "Europe",
            "countries": [{
                'country_code': 'FR',
                'language_code': 'en',
                'name': "France",
                'url': "http://en.wikipedia.org/wiki/France"
            }]
        }
        serializer = FlatContinentCountriesTranslatedSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        nested_data = serializer.validated_data['countries'][0]
        expected = data['countries'][0]
        self.assertDictEqual(nested_data, expected)
