from django.db import models

from admintools.models import CoreModel
from .parser import AbstractParser
from utils.pyppeteer import RESOURCE_TYPE


class NovelParser(AbstractParser):
    url = models.CharField(
        help_text='novel site url',
        max_length=100,
    )
    icon = models.ImageField(
        upload_to='site_icons/',
        help_text='site icon',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'NovelParser'
        verbose_name_plural = 'NovelParsers'

    def __str__(self) -> str:
        return self.name


class Resource(CoreModel):
    novel_parser = models.ForeignKey(
        NovelParser,
        on_delete=models.CASCADE,
    )
    urn = models.CharField(
        help_text='resource page urn',
        max_length=255,
    )
    urn_regex = models.CharField(
        help_text='necessary to resource search by income url',
        max_length=255,
        blank=True,
    )
    name = models.CharField(
        help_text='resource page name',
        max_length=100,
    )
    description = models.CharField(
        max_length=255,
        blank=True,
    )
    intercept_page_res = models.CharField(
        help_text=(f'put the types of resources that should not be '
                   f'loaded through "_"<br> for example: '
                   f'img_css_fetch_media_font_js<br>'
                   f'resource types: {", ".join(RESOURCE_TYPE.keys())}'),
        max_length=100,
        blank=True,
    )

    class Meta:
        verbose_name = 'Resource'
        verbose_name_plural = 'Resources'

    def __str__(self) -> str:
        return self.name
