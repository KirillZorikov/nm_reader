from django.db import models

from admintools.models import CoreModel
from parsers.models.settings import ParserSlugQuerySet


class Browser(CoreModel):
    """ chromium instance """
    wsEndpoint = models.CharField(
        help_text='address of the running browser',
        blank=True,
        max_length=255,
    )

    class Meta:
        verbose_name = 'Browser'
        verbose_name_plural = 'Browsers'

    def __str__(self) -> str:
        return self.wsEndpoint


class Page(CoreModel):
    """ browser page """
    browser = models.ForeignKey(
        Browser,
        on_delete=models.CASCADE,
    )
    parser = models.ForeignKey(
        'Parser',
        on_delete=models.CASCADE,
    )
    in_use = models.BooleanField(
        default=False,
    )
    index = models.PositiveSmallIntegerField(
        help_text='position at the browser\'s page list',
        unique=True,
    )
    fails_count = models.PositiveSmallIntegerField(
        help_text='the count of fails to get translate from the page',
        default=0,
    )

    objects = ParserSlugQuerySet.as_manager()

    def get_url(self):
        related_parser = self.parser.get_related_parser()
        return related_parser.url

    class Meta:
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'

    def __str__(self) -> str:
        return str(self.index)


class Block(CoreModel):
    """ css selector for block on the page """
    parser = models.ForeignKey(
        'Parser',
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        'block name',
        max_length=255,
    )
    description = models.CharField(
        max_length=255,
        blank=True,
    )
    css_selector = models.CharField(
        'block css selector',
        max_length=255,
    )

    objects = ParserSlugQuerySet.as_manager()

    class Meta:
        verbose_name = 'Block'
        verbose_name_plural = 'Blocks'

    def __str__(self) -> str:
        return self.name
