from pyppeteer.page import Page

from novels.utils import get_data_by_fields, split_by_fields


TITLE_FIELDS = [
    'author', 'author_link', 'title', 'title_link',
    'description', 'image', 'type',
    'style', 'status', 'words_count',
    'release_date', 'update_date', 'work_points',
    'last_chapter_link',
]


async def get_search_page_data(page: Page, blocks: dict, keywords: str, **kwargs):
    blocks = {key: val['selector'] for key, val in blocks.items()}
    data = await get_data_by_fields(
        page, blocks, kwargs['url'], TITLE_FIELDS
    )
    return split_by_fields(data)
