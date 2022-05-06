from pyppeteer import errors
from pyppeteer.page import Page

from .deepl import click_element, click_blank_area


async def choose_language(page: Page, blocks: dict, src: dict, dst: dict):
    # choose src lang
    await click_element(page, blocks['source_button'])
    await page.waitForSelector(src['source'])
    await click_element(page, src['source'], js_click=True)

    # close dropdown
    await click_blank_area(page, blocks)

    # choose dst lang
    await click_element(page, blocks['destination_button'])
    await page.waitForSelector(dst['destination'])
    await click_element(page, dst['destination'], js_click=True)

    # close dropdown
    await click_blank_area(page, blocks)


async def insert_data(page: Page, blocks: dict, data: str, **kwargs):
    text = '\n\n'.join(data)
    await click_element(page, blocks['textarea_container'], js_click=True)
    await page.evaluate(f'''
        document.querySelector('{blocks['textarea']}').value = `{text}`;
    ''')
    await click_element(page, blocks['textarea_container'], js_click=True)
    await page.keyboard.press('Enter', delay=200)
    await page.keyboard.up('Enter')
    await page.keyboard.press('Backspace', delay=200)
    await page.keyboard.up('Backspace')


async def clear_data(page: Page, blocks: dict):
    try:
        await click_element(page, blocks['clear_button'])
    except (errors.ElementHandleError, errors.PageError):
        await page.evaluate(f'''
            document.querySelector('{blocks['textarea']}').value = '';
        ''')
        await click_element(page, blocks['textarea_container'], js_click=True)
        await page.keyboard.press('Enter', delay=200)
        await page.evaluate(f'''
            document.querySelector('{blocks['result_block']}').innerHTML = '';
        ''')


async def get_translated_data(page: Page, blocks: dict):
    await page.waitForSelector(blocks['result_block'])
    element = await page.querySelector(blocks['result_block'])
    tr_text = await page.evaluate('(element) => element.innerText', element)
    return tr_text.strip().split('\n\n')
