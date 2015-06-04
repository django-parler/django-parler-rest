from django.contrib import admin
from parler.admin import TranslatableAdmin

from .models import Country

class CountryAdmin(TranslatableAdmin):
    pass

admin.site.register(Country, CountryAdmin)
