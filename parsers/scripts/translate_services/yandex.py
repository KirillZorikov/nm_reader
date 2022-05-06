import asyncio
from urllib.parse import urlparse
from urllib.parse import parse_qs

from pyppeteer import errors
from pyppeteer.page import Page

from .deepl import click_element


async def get_captcha_image_url(page, selector):
    image_elm = await page.querySelector(selector)
    return await page.evaluate('(element) => element.src', image_elm)


async def get_captcha_image(page: Page, captcha_data):
    # click button "i'm not robot"
    try:
        await click_element(page, captcha_data['captcha_button'])
    except errors.PageError:
        pass
    await page.waitForSelector(captcha_data['captcha_image'])

    # return captcha image
    return await get_captcha_image_url(page, captcha_data['captcha_image'])


async def enter_captcha(page: Page, solve: str, captcha_data: dict):
    captcha_input = await page.querySelector(captcha_data['captcha_input'])
    await captcha_input.type(solve)
    await click_element(page, captcha_data['captcha_result_button'])
    await page.waitForNavigation()
    success = 'showcaptcha' not in urlparse(page.url).path
    result = {'success': success}
    if not success:
        image_url = await get_captcha_image_url(page, captcha_data['captcha_image'])
        result.update({'new_image': image_url})
    return result


def get_lang_param(url: str):
    lang_param = ''
    parsed_url = urlparse(url)
    if 'lang' in parse_qs(parsed_url.query):
        lang_param = parse_qs(parsed_url.query)['lang'][0].strip()
    return lang_param


async def choose_language(page: Page, blocks: dict, src: dict, dst: dict):
    lang_param = get_lang_param(page.url)
    if not lang_param.startswith(src["code"]) and src["code"] != 'auto':
        await click_element(page, blocks['source_button'])
        await page.waitForSelector(src['source'])
        await click_element(page, src['source'], js_click=True)
    if not lang_param.endswith(dst["code"]):
        await click_element(page, blocks['destination_button'])
        await page.waitForSelector(dst['destination'])
        await click_element(page, dst['destination'], js_click=True)

    lang_param = get_lang_param(page.url)
    if not lang_param.endswith(dst["code"]):
        await choose_language(page, blocks, src, dst)
    await page.waitFor(300)


async def insert_data(page: Page, blocks: dict, data: list, **kwargs):
    text = '\n\n'.join(data)
    await click_element(page, blocks['textarea_container'])
    await page.evaluate(f'''
        document.querySelector('{blocks['textarea']}').value = `{text}`;
    ''')
    await page.waitFor(200)
    await page.keyboard.press('Enter', delay=200)
    await page.keyboard.up('Enter')
    await page.waitFor(200)
    await page.keyboard.press('Enter', delay=200)
    await page.keyboard.up('Enter')


async def clear_data(page: Page, blocks: dict):
    try:
        await click_element(page, blocks['clear_button'])
    except errors.ElementHandleError:
        await page.evaluate(f'''
            document.querySelector('{blocks['textarea']}').value = '';
        ''')
        await click_element(page, blocks['textarea_container'])
        await page.keyboard.press('Enter', delay=200)
    await page.evaluate(f'''
        document.querySelector('{blocks['result_block']}').innerHTML = '';
    ''')


async def get_text_from_result_block(page: Page, selector: str):
    element = await page.querySelector(selector)
    return await page.evaluate('(element) => element.textContent', element)


async def get_translated_data(page: Page, blocks: dict):
    tr_text = ''
    while not tr_text:
        await asyncio.sleep(0.05)
        tr_text = await get_text_from_result_block(page, blocks['result_block'])
        # print(tr_text, bool(tr_text))
        tr_text = tr_text.strip()
    return tr_text.strip().split('\n\n')
