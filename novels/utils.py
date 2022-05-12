import re

from pyppeteer.page import Page
from utils.url import is_absolute, join_url
from utils.pyppeteer import get_elements_attr, get_elements_text


def prepare_services_response(services: list) -> dict:
    new_services = {}
    for service in services:
        new_services.setdefault(service['code'], []).append(service)
    return new_services


async def get_links_obj(page: Page, selector):
    return await page.evaluate(f'''
        () => [...document.querySelectorAll(`{selector}`)].map(
            e => ({{
                text: e.textContent.trim(),
                link: e.tagName !== 'A'? e.querySelector('a').getAttribute(`href`): e.getAttribute(`href`)
            }})
        )
    ''')


async def get_links_data(page: Page, selector, url):
    links_obj = await get_links_obj(page, selector)
    links = []
    for obj in links_obj:
        href = obj['link']
        obj['link'] = href if is_absolute(
            href) else join_url(url, href)
        obj['text'] = re.sub('\s+', ' ', obj['text'])
        links.append(obj)
    return links


async def get_data_by_fields(page: Page, blocks, url, fields, single=False):
    data = {}
    for field in fields:
        if field not in blocks:
            continue
        if field.endswith('link'):
            data[field] = await get_links_data(page, blocks[field], url)
        elif field.endswith('image'):
            data[field] = await get_elements_attr(page, blocks[field], 'src')
        else:
            data[field] = await get_elements_text(page, blocks[field])
        if single:
            data[field] = data[field][0]
    return data


def split_by_fields(data: dict):
    fields = list(data.keys())
    if not fields:
        return data
    lengt = len(data[fields[0]])
    result = []
    for i in range(lengt):
        result.append({})
        for field in fields:
            try:
                result[-1][field] = data[field][i]
            except IndexError:
                continue
    return result