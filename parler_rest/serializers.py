"""
Custom serializers suitable to translated models.
"""
from rest_framework import serializers

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
