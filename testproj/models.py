from django.db import models
from django.utils.translation import gettext_lazy as _

from parler.models import TranslatableModel, TranslatedFields, TranslatedField, TranslatedFieldsModel


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


class Picture(TranslatableModel):

    """Picture database model."""

    image_nr = models.IntegerField(help_text="Just a dummy number")
    caption = TranslatedField()

    class Meta:
        verbose_name = _("picture")
        verbose_name_plural = _("pictures")

    def __str__(self):
        return self.caption


class PictureTranslation(TranslatedFieldsModel):
    master = models.ForeignKey(
        Picture,
        related_name='translations',
        on_delete=models.CASCADE,
    )

    caption = models.CharField(
        max_length=50,
    )

    class Meta:
        unique_together = [('language_code', 'master')]
