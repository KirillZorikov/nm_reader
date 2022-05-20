from operator import mod
from django.db import models
from django.db.models.query import QuerySet
from pytils.translit import slugify

from admintools.models import CoreModel
from parsers.models.browser import Browser
from parsers.models.settings import RelatedParserSlugQuerySet


class SiteLanguageQuerySet(QuerySet):
    def main(self):
        return self.filter(is_main=True).first()


class SiteLanguageManager(models.Manager):
    _queryset_class = SiteLanguageQuerySet


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
    novel_parser = models.OneToOneField(
        'NovelParser',
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
        return related_parser.slug if related_parser else f'{self.pk}'

    def get_related_parser(self):
        if self.translate_parser:
            return self.translate_parser
        elif self.translate_image_parser:
            return self.translate_image_parser
        elif self.novel_parser:
            return self.novel_parser


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


class SiteLanguage(CoreModel):
    """ language in which the site posts content """
    code = models.CharField(
        help_text='language code',
        max_length=10,
    )
    name = models.CharField(
        help_text='language name',
        max_length=100,
        blank=True,
    )
    flag = models.ImageField(
        upload_to='language_flags/',
        help_text='language flags',
        blank=True,
        null=True,
    )
    is_main = models.BooleanField(
        default=True,
    )

    objects = SiteLanguageManager()

    class Meta:
        verbose_name = 'SiteLanguage'
        verbose_name_plural = 'SiteLanguages'

    def __str__(self) -> str:
        return f'{self.code}'


class Search(CoreModel):
    parser = models.OneToOneField(
        Parser,
        on_delete=models.CASCADE,
    )
    search_query_param = models.CharField(
        max_length=100,
        blank=True,
    )
    use_POST = models.BooleanField(
        help_text='use POST request to search',
        default=False,
    )
    encoding = models.CharField(
        help_text=(
            'encode param by encoding scheme. '
            'for example: UTF-8 or GB2312. '
            'leave blank if doesnt need encoding.'
        ),
        max_length=20,
        blank=True,
    )

    class Meta:
        verbose_name = 'Search'
        verbose_name_plural = 'Search'

    def __str__(self) -> str:
        return f'{self.parser}__{self.id}'