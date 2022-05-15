"""
Custom serializers suitable to translated models.
"""
from django.core.exceptions import FieldDoesNotExist
from rest_framework import serializers
from parler.utils.i18n import get_language

# Similar to DRF itself, expose all fields in the same manner.
from parler_rest.fields import TranslatedFieldsField, TranslatedField, TranslatedAbsoluteUrlField  # noqa


class TranslatableModelSerializerMixin(object):
    """
    Mixin class to be added to a :class:`rest_framework.serializers.ModelSerializer` .
    """

    def save(self, **kwargs):
        """
        Extract the translations and save them after main object save.

        By default all translations will be saved no matter if creating
        or updating an object. Users with more complex needs might define
        their own save and handle translation saving themselves.
        """
        translated_data = self._pop_translated_data()
        instance = super(TranslatableModelSerializerMixin, self).save(**kwargs)
        self.save_translations(instance, translated_data)
        return instance

    def _pop_translated_data(self):
        """
        Separate data of translated fields from other data.
        """
        translated_data = {}
        for field_name, field in self.get_fields().items():
            if isinstance(field, (TranslatedField, TranslatedFieldsField)):
                key = field.source or field_name
                translations = self.validated_data.pop(key, None)
                if translations:
                    translated_data[key] = translations
        return translated_data

    def save_translations(self, instance, translated_data):
        """
        Save translation data into translation objects.
        """
        for meta in self.Meta.model._parler_meta:
            for field_name, translations in translated_data.items():
                for lang_code, translation in translations.items():
                    model_field = instance._get_translated_model(lang_code, auto_create=True, meta=meta)
                    if meta.rel_name == field_name:
                        for trans_field, value in translation.items():
                            setattr(model_field, trans_field, value)
                    elif field_name in meta.get_translated_fields():
                        setattr(model_field, field_name, translation)

        # Go through the same hooks as the regular model,
        # instead of calling translation.save() directly.
        instance.save_translations()


class TranslatableModelSerializer(TranslatableModelSerializerMixin, serializers.ModelSerializer):
    """
    Serializer that saves :class:`TranslatedFieldsField` automatically.
    """
    pass


class TranslatableFlatModelSerializer(TranslatableModelSerializerMixin, serializers.ModelSerializer):
    """
    Serializer that returns a flat model and saves the translations to the activated language.
    """

    def _pop_translated_data(self):
        translated_data = {}
        language_code = self.validated_data.pop('language_code', None) or get_language()
        translated_fields = self._pop_translatable_fields()
        for meta in self.Meta.model._parler_meta:
            translations = {}
            if translated_fields:
                translations[language_code] = translated_fields
                translated_data[meta.rel_name] = translations
        return translated_data

    def _pop_translatable_fields(self):
        """
        Separate translated fields and value from the shared object data.
        """
        translated_fields = {}
        fields = (field for field in self.Meta.model._parler_meta.get_all_fields()
                  if field in self.validated_data)
        for field in fields:
            translated_fields[field] = self.validated_data.pop(field)
        return translated_fields

    def build_field(self, field_name, info, model_class, nested_depth):
        """
        Build fields for translatable fields when not explicitly defined
        """
        field = None
        if field_name not in ('id', 'master'):
            try:
                field = model_class._parler_meta.root_model._meta.get_field(field_name)
            except FieldDoesNotExist:
                pass
        if field is not None:
            return self.build_standard_field(field_name, field)
        return super(TranslatableFlatModelSerializer, self).build_field(
         field_name, info, model_class, nested_depth)