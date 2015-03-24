from __future__ import unicode_literals

from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField

from .models import Country


class CountrySerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Country)

    class Meta:
        model = Country
        fields = ('id', 'country_code', 'translations')
