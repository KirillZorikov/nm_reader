from django.db import models
from django.db.models import UniqueConstraint

from admintools.models import CoreModel
from parsers.models.settings import ParserSlugQuerySet


class Browser(CoreModel):
    """ chromium instance """
    class BrowserParserType(models.TextChoices):
        TRANSLATE = 'Translate'
        NOVEL = 'Novel'

    type = models.CharField(
        max_length=50,
        choices=BrowserParserType.choices,
    )
    wsEndpoint = models.CharField(
        help_text='address of the running browser',
        blank=True,
        max_length=255,
    )

    class Meta:
        verbose_name = 'Browser'
        verbose_name_plural = 'Browsers'

    def __str__(self) -> str:
        return f'{self.type}__{self.wsEndpoint}'


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
    page_id = models.CharField(
        max_length=100,
        help_text='page id from the browser',
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
        constraints = [
            UniqueConstraint(
                'browser',
                'page_id',
                name='browser_page_id_unique',
            ),
        ]
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'

    def __str__(self) -> str:
        return str(self.page_id)


class Block(CoreModel):
    """ css selector for block on the page """
    parser = models.ForeignKey(
        'Parser',
        on_delete=models.CASCADE,
    )
    resource = models.ForeignKey(
        'Resource',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
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
    exclude_tags = models.BooleanField(
        help_text=(
            'if it has "bare text" then we should exclude other '
            'tags to get the proper innerText'
        ),
        default=False,
    )

    objects = ParserSlugQuerySet.as_manager()

    class Meta:
        verbose_name = 'Block'
        verbose_name_plural = 'Blocks'

    def __str__(self) -> str:
        if self.resource:
            return f'{self.parser}__{self.resource}__{self.name}'
        return f'{self.parser}__{self.name}'
