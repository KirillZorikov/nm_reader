import asyncio

from pyppeteer import errors
from pyppeteer.page import Page


async def click_element(page: Page, selector: str, js_click: bool = False):
    if js_click:
        await page.evaluate(f'document.querySelector(`{selector}`).click()')
    else:
        await page.click(selector)


async def click_blank_area(page: Page, blocks: dict):
    try:
        await click_element(page, blocks['blank_block'], js_click=True)
    except errors.ElementHandleError:
        pass


async def choose_language(page, blocks, src, dst):

    # choose src lang
    await click_element(page, blocks['source_button'], js_click=True)
    await page.waitForSelector(src['source'])
    await click_element(page, src['source'], js_click=True)

    # close dropdown
    await click_blank_area(page, blocks)

    # choose dst lang
    await click_element(page, blocks['destination_button'], js_click=True)
    await page.waitForSelector(dst['destination'])
    await click_element(page, dst['destination'], js_click=True)

    # close dropdown
    await click_blank_area(page, blocks)


async def insert_data(page, blocks, data, **kwargs):
    text = f'\n\n'.join(data)
    await click_element(page, blocks['textarea_container'])
    await page.evaluate(f'''
        document.querySelector('{blocks['textarea']}').value = `{text}`;
    ''')
    await page.click(blocks['textarea_container'], delay=50)
    await page.keyboard.press('Enter', delay=50)
    await page.keyboard.up('Enter')
    await page.waitFor(200)
    await page.keyboard.press('Backspace', delay=50)
    await page.keyboard.up('Backspace')


async def clear_data(page, blocks):
    try:
        await click_element(page, blocks['clear_button'])
        # await page.click(blocks['clear_button'])
    except (errors.ElementHandleError, errors.PageError):
        await page.evaluate(f'''
            document.querySelector('{blocks['textarea']}').value = '';
        ''')
        await click_element(page, blocks['textarea_container'])
        # await page.click(blocks['textarea_container'], delay=200)
        await page.keyboard.press('Enter', delay=200)
        await page.evaluate(f'''
            document.querySelector('{blocks['result_block']}').innerHTML = '';
        ''')


async def get_translated_data(page, blocks):
    tr_text = ''
    while not tr_text.strip():
        await asyncio.sleep(0.05)
        element = await page.querySelector(blocks['result_block'])
        tr_text = await page.evaluate('(element) => element.textContent', element)
    return tr_text.strip().split('\n\n')
