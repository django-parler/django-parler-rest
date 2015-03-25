# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from parler.models import TranslatableModel, TranslatedFields


@python_2_unicode_compatible
class Country(TranslatableModel):

    """Country database model."""

    country_code = models.CharField(_("country code"), max_length=2, unique=True, db_index=True)

    translations = TranslatedFields(
        name = models.CharField(_("name"), max_length=200),
        url = models.URLField(_("webpage"), max_length=200, blank=True),
    )

    class Meta:
        verbose_name = _("country")
        verbose_name_plural = _("countries")

    def __str__(self):
        return self.name
