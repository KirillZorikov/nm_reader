import asyncio

from urllib.parse import urlparse

from pyppeteer import connect
from .pyppeteer_stealth import stealth
from pyppeteer.browser import Browser
from pyppeteer.page import Page

from translate.scripts.translate_services import (
    deepl, yandex, google, yandex_image
)
from utils.browser import run_browser
from utils.pyppeteer import get_pages_dict
from translate import utils


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
    page_id=None,
    reload=False,
):
    if not page_id:
        return await run_new_page(browser, url)
    pages = await browser.pages()
    pages = get_pages_dict(pages)
    try:
        page = pages[page_id]
    except IndexError:
        return await browser.newPage()
    if reload:
        await page.reload()
    return page


async def translate(
    parser_data: dict,
    service: str,
    browser_endpoint=None,
    browser_id=None,
    page_id=None,
    *args,
    **kwargs,
):

    # prepare_browser_and_page
    browser = await get_browser(browser_endpoint)
    reload = kwargs.get('reload') or False
    url = parser_data['related_parser']['url']
    page = await get_page(
        browser, url,
        page_id, reload=reload
    )
    await stealth(page)
    await page.setViewport({'width': 1280, 'height': 720})
    # if urlparse(url).netloc not in page.url:
    if not page.url.startswith(url):
        await page.goto(url)
    # await page.setViewport({'width': 1280, 'height': 720})
    await page.screenshot({'path': f'temp_imgs/{page_id}_load_page.png'})
    
    # check_captcha
    if 'yandex' in service and 'showcaptcha' in page.url:
        image_url = await yandex.get_captcha_image(
            page, parser_data['captcha_data'][0]
        )
        return {
            'success': False,
            'message': 'captcha detected',
            'exception': utils.CaptchaDetectedAPIException(
                image_url, page_id=page_id,
                service_name=service, browser_id=browser_id,
            )
        }

    # choose_language
    src = next(x for x in parser_data['languages']
               if x['code'] == kwargs['src'])
    dst = next(x for x in parser_data['languages']
               if x['code'] == kwargs['dst'])
    await getattr(SERVICES[service], 'choose_language')(
        page, parser_data['blocks'], src, dst
    )
    await page.screenshot({'path': f'temp_imgs/{page_id}_choose_language.png'})

    # insert_data
    await getattr(SERVICES[service], 'insert_data')(
        page, parser_data['blocks'],
        kwargs['data'], unique=f'{page_id}_{browser_id}'
    )
    await page.screenshot({'path': f'temp_imgs/{page_id}_insert_data.png'})

    # wait_until_translate
    result = await getattr(SERVICES[service], 'get_translated_data')(
        page, parser_data['blocks']
    )
    await page.screenshot({'path': f'temp_imgs/{page_id}_wait_until_translate.png'})
    
    # clear_data
    await getattr(SERVICES[service], 'clear_data')(page, parser_data['blocks'])
    await page.screenshot({'path': f'temp_imgs/{page_id}_clear_data.png'})

    import os

    # os.remove(f'temp_imgs/{page_index}_clear_data.png')
    os.remove(f'temp_imgs/{page_id}_wait_until_translate.png')
    os.remove(f'temp_imgs/{page_id}_insert_data.png')
    os.remove(f'temp_imgs/{page_id}_choose_language.png')
    os.remove(f'temp_imgs/{page_id}_load_page.png')
    
    return {
        'success': True,
        'message': 'translated successfully',
        'data': result,
    }


async def solve_captcha(
    browser_endpoint: str,
    page_id: int,
    solve: str,
    captcha_parser_data: dict,
):
    browser = await get_browser(browser_endpoint)
    pages = await browser.pages()
    pages = get_pages_dict(pages)
    page = pages[page_id]
    await page.setViewport({'width': 1280, 'height': 720})
    result = await yandex.enter_captcha(page, solve, captcha_parser_data)
    result['message'] = 'captcha is solved'
    if not result['success']:
        result['message'] = 'captcha entered incorrectly'
    return result
