from rest_framework import viewsets

from .models import Country
from .serializers import CountryTranslatedSerializer, CountryHyperlinkedTranslatedSerializer


class CountryViewSet(viewsets.ModelViewSet):
    model = Country
    serializer_class = CountryTranslatedSerializer
    queryset = Country.objects.all()


class CountryHyperlinkedViewSet(viewsets.ModelViewSet):
    model = Country
    serializer_class = CountryHyperlinkedTranslatedSerializer
    queryset = Country.objects.all()