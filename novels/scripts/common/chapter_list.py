from pyppeteer.page import Page


from novels.utils import get_data_by_fields, split_by_fields


CHAPTER_LIST_FIELDS = [
    'number', 'name_link', 'name',
    'summary', 'words_count', 'update_date',
]
PAGINATOR_FIELDS = [
    'first_link', 'last_link', 'next_link', 'prev_link',
]
PAGINATOR_LIST_FIELDS = [
    'page_list_link', 'page_list_option',
]


async def get_paginator_data(page: Page, blocks, url):
    data = {}
    data.update(await get_data_by_fields(
        page, blocks, url, PAGINATOR_FIELDS, single=True
    ))
    data.update(await get_data_by_fields(
        page, blocks, url, PAGINATOR_LIST_FIELDS
    ))
    return data


async def get_chapter_list_page_data(page: Page, blocks: dict, **kwargs):
    blocks = {key: val['selector'] for key, val in blocks.items()}
    data = {}
    data['chapter_list_data'] = split_by_fields(await get_data_by_fields(
        page, blocks, kwargs['url'], CHAPTER_LIST_FIELDS
    ))
    data['paginator_data'] = split_by_fields(await get_paginator_data(
        page, blocks, kwargs['url']
    ))
    return data
