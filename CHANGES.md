# Changelog

## Changes in version 2.2 (2022-05-04)

* Drop support for Python-2.
* Add support for Python-3.8, 3.9 and 3.10.
* Drop support for Django 2.0 and 2.1.
* Add support for Django 3.2 and 4.0.


## Changes in version 2.1 (2020-01-09)

* Read/Write support for `TranslatedField`.
* Use composition instead of inheritance by moving funtionality from `TranslatableModelSerializer`
  into `TranslatableModelSerializerMixin`.
* Fix: Model check agianst `TranslatableModelMixin`.


## Changes in version 2.0 (2018-09-10)

* Added Django 2.0 and 2.1 support.
* Dropped Django 1.7, 1.8, 1.9, 1.10 support.


## Changes in version 1.4.2 (2016-06-17)

* Added type checking on the models used in the serializer.
  This avoids nasty errors when the shared model is used accidently.

For example, in Django 1.7 `MyModel.translations.related.model` resolved the translated model,
but on Django 1.8+ it returns the parent model. `MyModel.translations.related.related_model`
should be used instead.


## Changes in version 1.4.1 (2016-06-02)

* Make sure the model's `save_translations()` and `save_translation()` methods are called,
  in case those are overridden to provide extra changes.


## Changes in version 1.4 (2016-05-04)

* Added `languages` context variable to `TranslatedSerializer`.


## Changes in version 1.3 (2015-12-16)

* Fixed nested serializer support.
* Added `allow_empty` option to `parler_rest.fields.TranslatedFieldsField`.
  NOTE: by default, empty an empty `"translations": {}` value is no longer allowed.

### Released in 1.3b1

* Added support for [django-rest-framework](https://github.com/tomchristie/django-rest-framework) 3.
* Added `parler_rest.fields.TranslatedField` class to expose a single field in multiple languages (read only).
* Added `parler_rest.fields.TranslatedAbsoluteUrlField` class to expose a tranlated URL in a custom translations serializer.
* Support the `source` argument on the `TranslatedFieldsField`.
* Dropped support for [django-rest-framework](https://github.com/tomchristie/django-rest-framework) 2.


## Changes in version 1.2.1

* Fix djangorestframework PiPI package name in `setup.py`.


## Changes in version 1.2

* Initial release, extracted from [django-parler](https://github.com/django-parler/django-parler).
