# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField

from .models import Country


class CountryTranslatedSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Country)

    class Meta:
        model = Country
        fields = ('pk', 'country_code', 'translations')
