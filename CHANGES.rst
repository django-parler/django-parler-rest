Changelog
=========

Chages in version 1.3 (git)
---------------------------

* Added support for django-rest-framework_ 3.
* Added ``parler_rest.fields.TranslatedField`` class to expose a single field in multiple languages (read only).
* Added ``parler_rest.fields.TranslatedAbsoluteUrlField`` class to expose a tranlated URL in a custom translations serializer.
* Support the ``source`` argument on the ``TranslatedFieldsField``.
* Dropped support for django-rest-framework_ 2.


Changes in version 1.2.1
------------------------

* Fix djangorestframework PiPI package name in ``setup.py``.


Changes in version 1.2
----------------------

* Initial release, extracted from django-parler_ 1.2-git.


.. _django-parler: https://github.com/edoburu/django-parler
.. _django-rest-framework: https://github.com/tomchristie/django-rest-framework
