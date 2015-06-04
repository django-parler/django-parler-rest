# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from parler_rest import serializers
from rest_framework.serializers import HyperlinkedIdentityField

from .models import Country


class CountryTranslatedSerializer(serializers.TranslatableModelSerializer):
    translations = serializers.TranslatedFieldsField(shared_model=Country)

    class Meta:
        model = Country
        fields = ('id', 'country_code', 'translations')


class CountryHyperlinkedTranslatedSerializer(serializers.HyperlinkedTranslatableModelSerializer):
    url = HyperlinkedIdentityField(view_name='countryh-detail')

    translations = serializers.TranslatedFieldsField(shared_model=Country)

    class Meta:
        model = Country
        fields = ('url', 'country_code', 'translations')