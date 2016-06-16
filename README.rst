django-parler-rest
==================

.. image:: https://travis-ci.org/edoburu/django-parler-rest.svg?branch=master
    :target: http://travis-ci.org/edoburu/django-parler-rest
.. image:: https://img.shields.io/pypi/v/django-parler-rest.svg
    :target: https://pypi.python.org/pypi/django-parler-rest/
.. image:: https://img.shields.io/pypi/dm/django-parler-rest.svg
    :target: https://pypi.python.org/pypi/django-parler-rest/
.. image:: https://img.shields.io/badge/wheel-yes-green.svg
    :target: https://pypi.python.org/pypi/django-parler-rest/
.. image:: https://img.shields.io/pypi/l/django-parler-rest.svg
    :target: https://pypi.python.org/pypi/django-parler-rest/
.. image:: https://img.shields.io/codecov/c/github/edoburu/django-parler-rest/master.svg
    :target: https://codecov.io/github/edoburu/django-parler-rest?branch=master

Adding translation support to django-rest-framework_.

This package adds support for TranslatableModels from django-parler_ to django-rest-framework_.


Installation
============

::

    pip install django-parler-rest

Usage
=====

* First make sure you have django-parler_ installed and configured.
* Use the serializers as demonstrated below to expose the translations.

First configure a model, following the `django-parler documentation <https://django-parler.readthedocs.io/en/latest/>`_::

    from django.db import models
    from parler.models import TranslatableModel, TranslatedFields


    class Country(TranslatableModel):
        """
        Country database model.
        """

        country_code = models.CharField(_("Country code"), unique=True, db_index=True)

        translations = TranslatedFields(
            name = models.CharField(_("Name"), max_length=200)
            url = models.URLField(_("Webpage"), max_length=200, blank=True)
        )

        class Meta:
            verbose_name = _("Country")
            verbose_name_plural = _("Countries")

        def __unicode__(self):
            return self.name


The model translations can be exposed as a seperate serializer::

    from rest_framework import serializers
    from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField
    from .models import Country   # Example model


    class CountrySerializer(TranslatableModelSerializer):
        translations = TranslatedFieldsField(shared_model=Country)

        class Meta:
            model = Country
            fields = ('id', 'country_code', 'translations')


This will expose the fields as a separate dictionary in the JSON output::

    {
        "id": 528,
        "country_code": "NL",
        "translations": {
            "nl": {
                "name": "Nederland",
                "url": "http://nl.wikipedia.org/wiki/Nederland"
            },
            "en": {
                "name": "Netherlands",
                "url": "http://en.wikipedia.org/wiki/Netherlands"
            },
            "de" {
                "name": "Niederlande",
                "url": "http://de.wikipedia.org/wiki/Niederlande"
            }
        }
    }


Contributing
============

This module is designed to be generic. In case there is anything you didn't like about it,
or think it's not flexible enough, please let us know. We'd love to improve it!

If you have any other valuable contribution, suggestion or idea,
please let us know as well because we will look into it.
Pull requests are welcome too. :-)

Running tests
-------------

Tests are run with `py.test`::

    python setup.py test  # install dependencies and run tests with coverage


.. _django-parler: https://github.com/edoburu/django-parler
.. _django-rest-framework: http://www.django-rest-framework.org/
