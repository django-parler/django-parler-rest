from __future__ import absolute_import

from rest_framework import serializers

from parler_rest.fields import TranslatedFieldsField  # noqa


class TranslatableModelSerializer(serializers.ModelSerializer):

    """Serializer that saves the :class:`TranslatedFieldsField` properly.

    It should be used instead of the regular ``ModelSerializer``.
    """

    def save(self, **kwargs):
        """Extract the translations, store these into the django-parler model data."""
        translated_data = self._pop_translated_data()
        instance = super(TranslatableModelSerializer, self).save(**kwargs)
        self.save_translations(instance, translated_data)
        return instance

    def _pop_translated_data(self):
        translated_data = {}
        for meta in self.Meta.model._parler_meta:
            translations = self.validated_data.pop(meta.rel_name, {})
            if translations:
                translated_data[meta.rel_name] = translations
        return translated_data

    def save_translations(self, instance, translated_data):
        for meta in self.Meta.model._parler_meta:
            translations = translated_data.get(meta.rel_name, {})
            for lang_code, model_fields in translations.items():
                translation = instance._get_translated_model(lang_code, auto_create=True, meta=meta)
                for field, value in model_fields.items():
                    setattr(translation, field, value)
                translation.save()
