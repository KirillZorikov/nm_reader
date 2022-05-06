from urllib.parse import urlparse

from pyppeteer import connect
from .pyppeteer_stealth import stealth
from pyppeteer.browser import Browser
from pyppeteer.page import Page

from parsers.scripts.translate_services import (
    deepl, yandex, google, yandex_image
)
from parsers.scripts.browser import run_browser
from parsers import utils


SERVICES = {
    'deepl': deepl,
    'yandex': yandex,
    'google': google,
    'yandex-image': yandex_image,
}


async def get_browser(browser_endpoint: str = None):
    if not browser_endpoint:
        browser_endpoint = await run_browser()
    return await connect(browserWSEndpoint=browser_endpoint)


async def run_new_page(browser: Browser, url: str):
    page = await browser.newPage()
    await page.goto(url)
    return page


async def get_page(
    browser: Browser,
    url: str,
    page_index=None,
    ignore_exception=True,
    reload=False,
):
    if not page_index:
        return await run_new_page(browser, url)
    try:
        pages = await browser.pages()
        page = pages[page_index]
        if reload:
            await page.reload()
        if urlparse(url).netloc not in page.url:
            await page.goto(url)
        return page
    except IndexError as error:
        if not ignore_exception:
            raise error
        return await run_new_page(browser, url)


async def translate(
    parser_data: dict,
    service: str,
    browser_endpoint=None,
    browser_id=None,
    page_index=None,
    *args,
    **kwargs,
):

    # prepare_browser_and_page
    browser = await get_browser(browser_endpoint)
    reload = kwargs.get('reload') or False
    page = await get_page(
        browser, parser_data['related_parser']['url'],
        page_index, reload=reload
    )
    await page.setViewport({'width': 1280, 'height': 720})

    # check_captcha
    if 'yandex' in service and 'showcaptcha' in page.url:
        image_url = await yandex.get_captcha_image(
            page, parser_data['captcha_data'][0]
        )
        return {
            'success': False,
            'message': 'captcha detected',
            'exception': utils.CaptchaDetectedAPIException(
                image_url, page_index=page_index,
                service_name=service, browser_id=browser_id,
            )
        }

    # choose_language
    await stealth(page)
    src = next(x for x in parser_data['languages']
               if x['code'] == kwargs['src'])
    dst = next(x for x in parser_data['languages']
               if x['code'] == kwargs['dst'])
    await getattr(SERVICES[service], 'choose_language')(
        page, parser_data['blocks'], src, dst
    )

    # insert_data
    await getattr(SERVICES[service], 'insert_data')(
        page, parser_data['blocks'],
        kwargs['data'], unique=f'{page_index}_{browser_id}'
    )

    # wait_until_translate
    result = await getattr(SERVICES[service], 'get_translated_data')(
        page, parser_data['blocks']
    )

    # clear_data
    await getattr(SERVICES[service], 'clear_data')(page, parser_data['blocks'])

    return {
        'success': True,
        'message': 'translated successfully',
        'data': result,
    }


async def solve_captcha(
    browser_endpoint: str,
    page_index: int,
    solve: str,
    captcha_parser_data: dict,
):
    browser = await get_browser(browser_endpoint)
    pages = await browser.pages()
    page = pages[page_index]
    await page.setViewport({'width': 1280, 'height': 720})
    result = await yandex.enter_captcha(page, solve, captcha_parser_data)
    result['message'] = 'captcha is solved'
    if not result['success']:
        result['message'] = 'captcha entered incorrectly'
    return result
