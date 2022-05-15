from rest_framework import serializers

from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField, TranslatedField, \
    TranslatableFlatModelSerializer

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


class FlatCountryTranslatedSerializer(TranslatableFlatModelSerializer):
    """
    A serializer with a flat structure returning a single language for the translations
    """

    class Meta:
        model = Country
        fields = ('pk', 'country_code', 'language_code', 'name', 'url')


class FlatCountryExplicitLangTranslatedSerializer(TranslatableFlatModelSerializer):
    """
    A serializer where the possible language choice for the language_code field is explicit assigned
    """
    LANGUAGE_CHOICES = (
        ('en', 'english'),
        ('es', 'spanish'),
        ('fr', 'french'),
    )
    language_code = serializers.ChoiceField(choices=LANGUAGE_CHOICES)

    class Meta:
        model = Country
        fields = ('pk', 'country_code', 'language_code', 'name', 'url')


class FlatCountryNoLanguageCodeTranslatedSerializer(TranslatableFlatModelSerializer):
    """
    A serializer without a language_code field declared
    """

    class Meta:
        model = Country
        fields = ('pk', 'country_code', 'name', 'url')


class FlatContinentCountriesTranslatedSerializer(serializers.Serializer):
    """
    A flat serializer with a nested translation serializer
    """
    continent = serializers.CharField()
    countries = FlatCountryTranslatedSerializer(many=True)