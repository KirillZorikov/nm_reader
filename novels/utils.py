import re
from string import Formatter

from pyppeteer.page import Page
from utils.url import is_absolute, join_url
from utils.pyppeteer import get_elements_attr, get_elements_text


def prepare_services_response(services: list) -> dict:
    new_services = {}
    for service in services:
        new_services.setdefault(service['code'], []).append(service)
    return new_services


async def get_links_obj(page: Page, selector, option):
    func_data = {}
    func_data['tag_name'] = 'OPTION' if option else 'A'
    func_data['val_attr'] = 'value' if option else 'href'
    return await page.evaluate(f'''
        (func_data) => [...document.querySelectorAll(`{selector}`)].map(
            e => ({{
                text: e.textContent.trim(),
                link: e.tagName !== func_data['tag_name']? e.querySelector(func_data['tag_name']).getAttribute(func_data['val_attr']): e.getAttribute(func_data['val_attr'])
            }})
        )
    ''', func_data)


async def get_links_data(page: Page, selector, url, option=False):
    links_obj = await get_links_obj(page, selector, option)
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
        elif field.endswith('option'):
            data[field] = await get_links_data(page, blocks[field], url, option=True)
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
            except (IndexError, KeyError):
                continue
    return result


def get_additional_info(**kwargs):
    data = {}
    data['novel_id'] = kwargs.get('novel_id')
    data['chapter_id'] = kwargs.get('chapter_id')
    data['keywords'] = kwargs.get('keywords')
    data['lang_code'] = kwargs['query_params']['lang_code']
    data['service_name'] = kwargs['query_params']['service']
    data['resource_name'] = kwargs['query_params']['resource_name']
    if 'author_page' in data['resource_name']:
        data['author_id'] = kwargs.get('data')
    if 'novel_page' in data['resource_name']:
        data['title_id'] = kwargs.get('data')
    return {
        'request_info': {key: val for key, val in data.items() if val}
    }


def get_string_format_keys(string):
    keys = [t[1] for t in Formatter().parse(string) if t[1] is not None]
    return keys