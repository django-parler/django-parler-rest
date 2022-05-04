# django-parler-rest

**Adding translation support to [django-rest-framework](http://www.django-rest-framework.org/)**.

[![Tests](https://github.com/django-parler/django-parler-rest/actions/workflows/tests.yml/badge.svg)](https://github.com/django-parler/django-parler-rest/actions/workflows/tests.yml)
[![PyPI](https://img.shields.io/pypi/pyversions/django-parler-rest.svg)](https://pypi.python.org/pypi/django-parler-rest)
[![PyPI version](https://img.shields.io/pypi/v/django-parler-rest.svg)](https://pypi.python.org/pypi/django-parler-rest)
[![License](https://img.shields.io/pypi/l/django-parler-rest.svg)](https://pypi.python.org/pypi/django-parler-rest)
[![Coverage](https://img.shields.io/codecov/c/github/django-parler/django-parler-rest/master.svg)](https://codecov.io/github/django-parler/django-parler-rest?branch=master)

This package adds support for TranslatableModels from [django-parler](https://github.com/django-parler/django-parler)
to [django-rest-framework](http://www.django-rest-framework.org/).


## Installation

```shell
pip install django-parler-rest
```


## Usage

* First make sure you have django-parler_ installed and configured.
* Use the serializers as demonstrated below to expose the translations.

First configure a model, following the [django-parler documentation](https://django-parler.readthedocs.io/en/latest/):

```python
from django.db import models
from django.utils.translation import gettext_lazy as _

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

    def __str__(self):
        return self.name
```

The model translations can be exposed as a separate serializer:

```python
from rest_framework import serializers
from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField
from .models import Country  # Example model


class CountrySerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Country)

    class Meta:
        model = Country
        fields = ('id', 'country_code', 'translations')
```

**Note:** The `TranslatedFieldsField` can only be used in a serializer that inherits from
`TranslatableModelSerializer`.


This will expose the fields as a separate dictionary in the JSON output:

```json
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
        "de": {
            "name": "Niederlande",
            "url": "http://de.wikipedia.org/wiki/Niederlande"
        }
    }
}
```

## Contributing

This module is designed to be generic. In case there is anything you didn't like about it,
or think it's not flexible enough, please let us know. We'd love to improve it!

If you have any other valuable contribution, suggestion or idea,
please let us know as well because we will look into it.
Pull requests are welcome too. :-)


## Running tests

Tests are run with `py.test`:

```shell
python setup.py test  # install dependencies and run tests with coverage
```
