from pyppeteer.page import Page

from novels.utils import (
    get_data_by_fields, 
    split_by_fields, 
    get_additional_info,
)

TITLE_FIELDS = [
    'title', 'author', 'author_link',
    'image', 'description', 'status',
    'chapters_count', 'last_chapter_link',
    'update_data',
]
CHAPTER_LIST_FIELDS = [
    'chapter_number', 'chapter_name_link', 'chapter_name',
    'chapter_summary', 'chapter_words_count', 'chapter_update_date',
]


async def get_novel_page_data(page: Page, blocks: dict, **kwargs):
    blocks = {key: val['selector'] for key, val in blocks.items()}
    data = {}
    data['title_data'] = await get_data_by_fields(
        page, blocks, kwargs['url'], TITLE_FIELDS, single=True
    )
    data['chapter_list_data'] = split_by_fields(await get_data_by_fields(
        page, blocks, kwargs['url'], CHAPTER_LIST_FIELDS
    ))
    data.update(get_additional_info(**kwargs))
    return data
