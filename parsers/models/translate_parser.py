from django.db import models

from admintools.models import CoreModel
from parsers.models.parser import AbstractParser, Parser
from parsers.models.settings import ParserSlugQuerySet


class Language(CoreModel):
    """Language options for the translate parser"""
    parser = models.ForeignKey(
        'Parser',
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        'Language name',
        max_length=100,
    )
    code = models.CharField(
        'Language code',
        max_length=10,
    )
    source = models.CharField(
        help_text='language selector from the drop-down menu',
        max_length=255,
        blank=True,
    )
    destination = models.CharField(
        help_text='language selector from the drop-down menu',
        max_length=255,
        blank=True,
    )

    objects = ParserSlugQuerySet.as_manager()

    class Meta:
        verbose_name = 'Language'
        verbose_name_plural = 'Languages'

    def __str__(self) -> str:
        return self.name


class TranslateParser(AbstractParser):
    url = models.CharField(
        help_text='translator website',
        max_length=255,
    )

    class Meta:
        verbose_name = 'TranslateParser'
        verbose_name_plural = 'TranslateParsers'

    def __str__(self) -> str:
        return self.url


class TranslateImageParser(AbstractParser):
    """ Yandex Image Translate """
    url = models.CharField(
        help_text='image translator website',
        max_length=255,
    )
    file_input = models.CharField(
        help_text='file input selector',
        max_length=255,
    )

    class Meta:
        verbose_name = 'TranslateImageParser'
        verbose_name_plural = 'TranslateImageParsers'

    def __str__(self) -> str:
        return self.url


class Captcha(CoreModel):
    parser = models.ForeignKey(
        Parser,
        on_delete=models.CASCADE,
    )
    captcha_button = models.CharField(
        help_text='captcha button selector(i\'m not robot)',
        max_length=255,
    )
    captcha_image = models.CharField(
        help_text='captcha image selector',
        max_length=255,
    )
    captcha_input = models.CharField(
        help_text='captcha input selector',
        max_length=255,
    )
    captcha_result_button = models.CharField(
        help_text='captcha result button selector',
        max_length=255,
    )

    objects = ParserSlugQuerySet.as_manager()

    class Meta:
        verbose_name = 'Captcha'
        verbose_name_plural = 'Captcha'
