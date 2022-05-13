import asyncio
import os

from pyppeteer import errors
from pyppeteer.page import Page
from PIL import Image

from .deepl import click_element


def save_file(file, filename, dir):
    try:
        os.mkdir(dir)
    except FileExistsError:
        pass
    image = Image.open(file)
    image.save(os.path.join(dir, filename))


async def insert_data(page: Page, blocks: dict, data, **kwargs):
    dir = './temp_imgs'
    filename = kwargs['unique'] + data.name[data.name.rindex('.'):]
    save_file(data.file, filename, dir)
    input_element = await page.querySelector(blocks['file_input'])
    await input_element.uploadFile(os.path.join(dir, filename))
    # delete_file(filename, dir)


async def choose_language(page: Page, blocks: dict, src: dict, dst: dict):
    await click_element(page, blocks['source_button'])
    await click_element(page, src['source'], js_click=True)
    await click_element(page, blocks['destination_button'])
    await click_element(page, dst['destination'], js_click=True)


async def clear_data(page, blocks):
    try:
        await click_element(page, blocks['clear_button'])
    except (errors.ElementHandleError, errors.PageError):
        await page.evaluate(f'''
            document.querySelector('{blocks['textarea']}').value = '';
        ''')
        await click_element(page, blocks['textarea_container'])
        await page.keyboard.press('Enter', delay=200)
        await page.evaluate(f'''
            document.querySelector('{blocks['result_block']}').innerHTML = '';
        ''')


async def wait_for_failure(page):
    try:
        await page.waitForResponse(lambda res: res.status == 429, timeout=3000)
    except asyncio.TimeoutError:
        await asyncio.sleep(10)
    return {
        'success': False,
        'message': 'failed to recognize and translate text'
    }


async def wait_for_success(page):
    ocr_url = 'https://translate.yandex.net/ocr/'
    trans_url = 'https://translate.yandex.net/api/v1/tr.json/translate'
    ocr = await page.waitForResponse(lambda res: str(res.url).startswith(ocr_url))
    translate = await page.waitForResponse(lambda res: str(res.url).startswith(trans_url))
    return {
        'success': True,
        'ocr_data': await ocr.json(),
        'translate_data': await translate.json(),
    }


async def get_translated_data(page: Page, blocks):
    success = asyncio.create_task(wait_for_success(page))
    failure = asyncio.create_task(wait_for_failure(page))

    done_first, pending = await asyncio.wait(
        {success, failure}, return_when=asyncio.FIRST_COMPLETED
    )
    if isinstance(done_first, set):
        done_first = list(done_first)[0]
    return done_first.result()
