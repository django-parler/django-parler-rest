from __future__ import absolute_import

from rest_framework import serializers

from parler_rest.fields import TranslatedFieldsField  # noqa


class TranslatableModelSerializer(serializers.ModelSerializer):

    """Serializer that saves the :class:`TranslatedFieldsField` properly.

    It should be used instead of the regular ``ModelSerializer``.
    """

    def save(self, **kwargs):
        """Extract the translations, store these into the django-parler model data."""
        self._parler_translations = self._pop_translated_data()

        instance = super(TranslatableModelSerializer, self).save(**kwargs)

        # TODO: Save translations
        # translations = obj._related_data.pop(meta.rel_name, {})
        #     if translations:
        #         for lang_code, model_fields in translations.iteritems():
        #             translations = obj._get_translated_model(lang_code, auto_create=True, meta=meta)
        #             for field, value in model_fields.iteritems():
        #                 setattr(translations, field, value)
        return instance

    def _pop_translated_data(self, **kwargs):
        parler_translations = {}
        for meta in self.Meta.model._parler_meta:
            translations = kwargs.pop(meta.rel_name, {})
            if translations:
                parler_translations[meta.rel_name] = translations
        return parler_translations
