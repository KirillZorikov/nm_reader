import os
import websockets
import asyncio
import time
import datetime
from urllib.parse import urlparse

from pyppeteer import launch, connect
from pyppeteer.browser import Browser as PyppeteerBrowser
from pyppeteer.page import Page as PyppeteerPage
from django.db.utils import OperationalError
from django.utils import timezone
from django.db import transaction
from django.db.models import Q, QuerySet

from parsers.models import Browser, Page, Parser, ParserSettings
from translate.utils import run_async2
from utils.pyppeteer import get_pages_dict


MAX_TABS_PER_SERVICE = 6


async def make_new_page(endpoint: str) -> PyppeteerPage:
    browser = await connect(browserWSEndpoint=endpoint)
    page = await browser.newPage()
    return page


async def get_browser_pages(endpoint: str) -> list:
    browser = await connect(browserWSEndpoint=endpoint)
    return await browser.pages()


def create_pages(browser: Browser, service_name, count=0):
    max_count = get_page_limits().get(service_name) or count
    if count:
        max_count = min(count, max_count)
    pages_id = []
    for _ in range(max_count):
        br_page = asyncio.run(run_async2(make_new_page, endpoint=browser.wsEndpoint))
        page = ''
        while not page:
            try:
                page, _ = Page.objects.update_or_create(
                    browser=browser,
                    parser=Parser.objects.annotate_related_parser_slug().filter(
                        related_parser_slug=service_name
                    ).first(),
                    page_id=br_page.mainFrame._id
                )
                pages_id.append(page.page_id)
            except OperationalError:
                time.sleep(0.01)
    return pages_id


def check_pages_created(parser: Parser, service_name):
    browser = Browser.objects.filter(type=parser.type).last()
    if not browser:
        return False
    running_browser = asyncio.run(run_async2(
        return_running,
        endpoint=browser.wsEndpoint,
    ))
    if not isinstance(running_browser, PyppeteerBrowser):
        return False
    print(parser.page_set.count())
    print(get_page_limits().get(service_name))
    return parser.page_set.count() >= get_page_limits().get(service_name)


async def run_browser() -> str:
    kwargs = {
        'args': [
            '--window-size=1280,720',
            '--no-sandbox',
            '--ignore-certificate-errors',
            '--disable-accelerated-2d-canvas',
            '--disable-gpu',
            # '--user-data-dir=C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\User Data'
        ],
        'handleSIGINT': False,
        'handleSIGTERM': False,
        'handleSIGHUP': False,
        'autoClose': True,
        'headless': True,
        'ignoreHTTPSErrors': True,
        'defaultViewport': {
            'width': 1280,
            'height': 720
        }
    }
    chrome_path = os.environ.get('CHROME_PATH', default='')
    chrome_path = r'/usr/bin/google-chrome-stable'
    # chrome_path = r'/mnt/c/Program Files/Google/Chrome/Application/chrome.exe'
    # chrome_path = r'/mnt/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
    if chrome_path:
        kwargs.update({'executablePath': chrome_path})
    browser = await launch(**kwargs)
    return browser.wsEndpoint


async def check_connection(url, data=''):
    websocket = await websockets.connect(url)
    await websocket.close()


async def return_running(endpoint: str) -> PyppeteerBrowser:
    browser = ''
    try:
        await check_connection(endpoint)
        browser = await connect(browserWSEndpoint=endpoint)
    except ConnectionRefusedError:
        pass
    return browser


async def kill_browser(endpoint: str):
    browser = await connect(browserWSEndpoint=endpoint)
    return await browser.close()


def get_pages_by_service_name(service_name: str) -> QuerySet:
    return Page.objects.annotate_parser_slug().filter(
        parser_slug=service_name
    )


def get_page_limits() -> dict:
    parser_settings = ParserSettings.objects.first()
    return {
        'deepl': parser_settings.max_tab_deepl,
        'yandex': parser_settings.max_tab_yandex,
        'yandex-image': parser_settings.max_tab_yandex_image,
        'google': parser_settings.max_tab_google,
    }


@transaction.atomic
def get_page(browser: Browser, service_name: str) -> Page:
    parser = Parser.objects.annotate_related_parser_slug().filter(
        related_parser_slug=service_name
    ).first()
    count = Page.objects.filter(browser=browser).count()

    # zero tabs yet => open new
    if get_pages_by_service_name(service_name).count() == 0:
        p = asyncio.run(run_async2(make_new_page, endpoint=browser.wsEndpoint))
        page = Page.objects.create(
            browser=browser,
            parser=parser,
            page_id=p.mainFrame._id,
            in_use=True,
        )
        return page

    # not zero tabs => looking for free one
    timeout = ParserSettings.objects.first().timeout
    recently_updated = Q(
        updated__lte=timezone.now() - datetime.timedelta(seconds=timeout)
    )
    in_use = Q(in_use=True)
    if get_pages_by_service_name(service_name).filter(
        in_use & ~recently_updated
    ).count() >= (get_page_limits().get(service_name) or MAX_TABS_PER_SERVICE):
        return
    pages = get_pages_by_service_name(service_name)
    pages_filter = pages.filter(~in_use | recently_updated)
    page = pages_filter.first()
    if not page:
        p = asyncio.run(run_async2(make_new_page, endpoint=browser.wsEndpoint))
        page = Page.objects.create(
            browser=browser,
            parser=parser,
            page_id=p.mainFrame._id,
            in_use=True,
        )
        return page
    page.in_use = True
    page.save()
    return page


def clear_page_table():
    Page.objects.all().delete()


def check_recently_update(type='Translate'):
    browser = Browser.objects.filter(type=type).last()
    if browser:
        return browser.is_recently_updated, browser.wsEndpoint
    return None, None


async def check_page_open(
    page_id: int,
    endpoint: str,
    service_url: str,
    yandex_captcha_check=False
) -> bool:
    pages = await get_browser_pages(endpoint)
    pages = get_pages_dict(pages)
    if page_id not in pages:
        return False
    page = pages[page_id]
    check_url = urlparse(service_url).netloc in urlparse(page.url).netloc
    check_captcha = 'showcaptcha' in page.url if yandex_captcha_check else True
    return check_url and check_captcha


def get_browser(type, service_name) -> Browser:
    browser = Browser.objects.filter(type=type).last()
    if not browser:
        clear_page_table()
        wsEndpoint = asyncio.run(run_async2(run_browser))
        browser = Browser.objects.create(
            wsEndpoint=wsEndpoint,
            type=type,
        )
        return browser
    running_browser = asyncio.run(run_async2(
        return_running,
        endpoint=browser.wsEndpoint,
    ))
    if not isinstance(running_browser, PyppeteerBrowser):
        clear_page_table()
        recently_updated, wsEndpoint = check_recently_update()
        if not recently_updated:
            wsEndpoint = asyncio.run(run_async2(run_browser))
            browser.wsEndpoint = wsEndpoint
            browser.save()
    return browser


def prepare_browser(service_name: str, page_index=None, type='Novel'):
    browser = get_browser(type, service_name)
    page = ''
    while not page:
        try:
            page = get_page(browser, service_name)
        except OperationalError:
            pass
        time.sleep(0.5)
    print(f'PAGE - {page}')
    return browser, page
