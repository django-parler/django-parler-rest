from rest_framework import serializers

from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField, TranslatedField

from .models import Country, Picture


class CountryTranslatedSerializer(TranslatableModelSerializer):
    """
    A serializer with translated fields deduced and translation model explicitly declared.
    """

    translations = TranslatedFieldsField(shared_model=Country)

    class Meta:
        model = Country
        fields = ('pk', 'country_code', 'translations')


class CountryAutoSharedModelTranslatedSerializer(TranslatableModelSerializer):
    """
    A serializer with both translated fields and translation model deduced.
    """

    translations = TranslatedFieldsField()

    class Meta:
        model = Country
        fields = ('pk', 'country_code', 'translations')


class CountryExplicitTranslatedSerializer(TranslatableModelSerializer):
    """
    A serializer with explicit translation serializer.
    """

    class CountryTranslatedFieldsSerializer(serializers.ModelSerializer):
        class Meta:
            model = Country._parler_meta.root_model
            fields = ("name",)  # Skip url for the hell of it

    trans = TranslatedFieldsField(serializer_class=CountryTranslatedFieldsSerializer, source="translations")

    class Meta:
        model = Country
        fields = ('pk', 'country_code', 'trans')


class ContinentCountriesTranslatedSerializer(serializers.Serializer):
    """
    A serializer with a nested translation serializer.
    """

    continent = serializers.CharField()
    countries = CountryTranslatedSerializer(many=True)


class PictureCaptionSerializer(TranslatableModelSerializer):
    """
    A serializer with one translated field.
    """

    caption = TranslatedField()

    class Meta:
        model = Picture
        fields = ('image_nr', 'caption')
