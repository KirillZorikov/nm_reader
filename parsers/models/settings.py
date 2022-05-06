import asyncio

from django.db import models
from django.db.models import Case, When
from django.dispatch import receiver
from django.db.models.signals import post_save
from preferences.models import Preferences
from pyppeteer.browser import Browser as PyppeteerBrowser


class ParserSlugQuerySet(models.QuerySet):
    def annotate_parser_slug(self):
        return self.annotate(
            parser_slug=Case(
                When(
                    parser__translate_parser__isnull=False,
                    then='parser__translate_parser__slug'
                ),
                When(
                    parser__translate_image_parser__isnull=False,
                    then='parser__translate_image_parser__slug'
                ),
            )
        )


class RelatedParserSlugQuerySet(models.QuerySet):
    def annotate_related_parser_slug(self):
        return self.annotate(
            related_parser_slug=Case(
                When(
                    translate_parser__isnull=False,
                    then='translate_parser__slug'
                ),
                When(
                    translate_image_parser__isnull=False,
                    then='translate_image_parser__slug'
                ),
            )
        )


class ParserSettings(Preferences):
    max_tab_deepl = models.PositiveSmallIntegerField(
        help_text='how many tabs will be open for the deepl translator',
        default=4,
    )
    max_tab_google = models.PositiveSmallIntegerField(
        help_text='how many tabs will be open for the google translator',
        default=4,
    )
    max_tab_yandex = models.PositiveSmallIntegerField(
        help_text='how many tabs will be open for the yandex translator',
        default=4,
    )
    max_tab_yandex_image = models.PositiveSmallIntegerField(
        help_text='how many tabs will be open for the yandex-image translator',
        default=4,
    )
    timeout = models.PositiveSmallIntegerField(
        help_text="how many seconds will the tab be running before TimeoutException",
        default=40,
    )

    class Meta:
        verbose_name = 'ParserSettings'
        verbose_name_plural = 'ParserSettings'


@receiver(post_save, sender=ParserSettings)
def post_save_parser_settings(sender, instance, *args, **kwargs):
    from parsers.scripts.browser import (
        kill_browser, return_running, run_browser, init_pages
    )
    from parsers.models.browser import Browser
    from parsers.utils import run_async2

    browser = Browser.objects.last()
    if not browser:
        return
    running_browser = asyncio.run(run_async2(
        return_running,
        endpoint=browser.wsEndpoint,
        timeout=2.0
    ))
    if not isinstance(running_browser, PyppeteerBrowser):
        return
    asyncio.run(run_async2(
        kill_browser,
        endpoint=running_browser.wsEndpoint,
    ))
    wsEndpoint = asyncio.run(run_async2(run_browser))
    browser.wsEndpoint = wsEndpoint
    browser.save()
    init_pages(browser)
