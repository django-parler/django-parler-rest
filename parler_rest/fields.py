# -*- coding: utf-8 -*-
"""
Custom serializer fields for nested translations.
"""
from __future__ import unicode_literals
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.fields import SkipField
from parler.models import TranslatableModel, TranslatedFieldsModel
from parler.utils.context import switch_language

from parler_rest.utils import create_translated_fields_serializer

try:
    from collections import OrderedDict
except ImportError:
    from django.utils.datastructures import SortedDict as OrderedDict


class TranslatedFieldsField(serializers.Field):
    """
    Exposing all translated fields for a TranslatableModel in REST style.
    """
    default_error_messages = dict(serializers.Field.default_error_messages, **{
        'invalid': _("Input is not a valid dict"),
        'empty': _("This field may not be empty.")
    })

    def __init__(self, *args, **kwargs):
        """
        Receive custom serializer class and model.
        """
        self.serializer_class = kwargs.pop('serializer_class', None)
        self.shared_model = kwargs.pop('shared_model', None)

        self.allow_empty = kwargs.pop('allow_empty', False)
        super(TranslatedFieldsField, self).__init__(*args, **kwargs)

    def bind(self, field_name, parent):
        """
        Create translation serializer dynamically.

        Takes translatable model class (shared_model) from parent serializer and it
        may create a serializer class on the fly if no custom class was specified.
        """
        if not issubclass(parent.Meta.model, TranslatableModel):
            raise TypeError("Expected 'TranslatableModel' for the parent model")

        super(TranslatedFieldsField, self).bind(field_name, parent)

        # Expect 1-on-1 for now. Allow using source as alias,
        # but it should not be a dotted path for now
        related_name = self.source or field_name

        # This could all be done in __init__(), but by moving the code here,
        # it's possible to auto-detect the parent model.
        if self.shared_model is not None and self.serializer_class is not None:
            return

        # Fill in the blanks
        if self.serializer_class is None:
            # Auto detect parent model
            if self.shared_model is None:
                self.shared_model = parent.Meta.model

            # Create serializer based on shared model.
            translated_model = self.shared_model._parler_meta[related_name]
            self.serializer_class = create_translated_fields_serializer(
                self.shared_model, related_name=related_name,
                meta={'fields': translated_model.get_translated_fields()}
            )
        else:
            if not issubclass(self.serializer_class.Meta.model, TranslatedFieldsModel):
                raise TypeError("Expected 'TranslatedFieldsModel' for the serializer model")

            # On Django 1.8+ this works:
            #translated_fields_model = self.serializer_class.Meta.model
            #self.shared_model = translated_fields_model.master.field.related.model

    def to_representation(self, value):
        """
        Serialize translated fields.

        Simply iterate over available translations and, for each language,
        delegate serialization logic to the translation model serializer.

        Output languages can be selected by passing a list of language codes,
        `languages`, within the serialization context.
        """
        if value is None:
            return

        # Only need one serializer to create the native objects
        serializer = self.serializer_class(
            instance=self.parent.instance,  # Typically None
            context=self.context,
            partial=self.parent.partial
        )

        # Don't need to have a 'language_code', it will be split up already,
        # so this should avoid redundant output.
        if 'language_code' in serializer.fields:
            raise ImproperlyConfigured("Serializer may not have a 'language_code' field")

        translations = value.all()  # value = translations related manager
        languages = self.context.get('languages')
        if languages:
            translations = translations.filter(language_code__in=languages)

        # Split into a dictionary per language
        result = OrderedDict()
        for translation in translations:
            result[translation.language_code] = serializer.to_representation(translation)

        return result

    def to_internal_value(self, data):
        """
        Deserialize data from translations fields.

        For each received language, delegate validation logic to
        the translation model serializer.
        """
        if data is None:
            return

        if not isinstance(data, dict):
            self.fail('invalid')
        if not self.allow_empty and len(data) == 0:
            self.fail('empty')

        result, errors = {}, {}
        for lang_code, model_fields in data.items():
            serializer = self.serializer_class(data=model_fields)
            if serializer.is_valid():
                result[lang_code] = serializer.validated_data
            else:
                errors[lang_code] = serializer.errors

        if errors:
            raise serializers.ValidationError(errors)
        return result


class TranslatedField(serializers.ReadOnlyField):
    """
    Read-only field to expose a single object property in all it's languages.
    """

    def get_attribute(self, instance):
        # Instead of fetching the attribute with getattr() (that proxies to the Parler TranslatableField),
        # read the translation model directly to fetch all languages, and combine that into a dict.
        model = instance._parler_meta.get_model_by_field(self.source)  # This already validates the fields existance
        extension = instance._parler_meta[model]
        translations = getattr(instance, extension.rel_name)

        # Split into a dictionary per language
        value = OrderedDict()
        for translation in translations.all():  # Allow prefetch_related() to do it's work
            value[translation.language_code] = getattr(translation, self.source)
        return value

    def to_representation(self, value):
        return value


class TranslatedAbsoluteUrlField(serializers.ReadOnlyField):
    """
    Allow adding an absolute URL to a given translation.
    """
    def get_attribute(self, instance):
        # When handling the create() all, skip this field.
        if isinstance(instance, (dict, OrderedDict)):
            raise SkipField()

        assert isinstance(instance, TranslatedFieldsModel), (
            ("The TranslatedAbsoluteUrlField can only be used on a TranslatableModelSerializer, "
             " not on a {0}".format(instance.__class__))
        )

        return instance

    def to_representation(self, value):
        request = self.context['request']
        with switch_language(value.master, value.language_code):
            return request.build_absolute_uri(value.master.get_absolute_url())
