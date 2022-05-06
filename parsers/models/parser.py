from django.db import models
from pytils.translit import slugify

from admintools.models import CoreModel
from parsers.models.browser import Browser
from parsers.models.settings import RelatedParserSlugQuerySet


class Parser(CoreModel):
    class ParserType(models.TextChoices):
        TRANSLATE = 'Translate'
        TRANSLATE_IMAGE = 'TranslateImage'
        NOVEL = 'Novel'

    type = models.CharField(
        max_length=50,
        choices=ParserType.choices,
    )
    translate_parser = models.OneToOneField(
        'TranslateParser',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    translate_image_parser = models.OneToOneField(
        'TranslateImageParser',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    objects = RelatedParserSlugQuerySet.as_manager()

    class Meta:
        verbose_name = 'Parser'
        verbose_name_plural = 'Parsers'

    def __str__(self) -> str:
        related_parser = self.get_related_parser()
        return related_parser.name if related_parser else f'{self.pk}'

    def get_related_parser(self):
        if self.translate_parser:
            return self.translate_parser
        elif self.translate_image_parser:
            return self.translate_image_parser


class AbstractParser(CoreModel):
    browser = models.ForeignKey(
        Browser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    name = models.CharField(
        max_length=100,
    )
    slug = models.SlugField(
        max_length=50,
        blank=True,
        help_text='unique key for url generation'
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
