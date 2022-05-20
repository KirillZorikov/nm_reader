from pyppeteer.page import Page


from novels.utils import (
    get_data_by_fields, 
    split_by_fields, 
    get_additional_info
)


TITLE_FIELDS = [
    'author', 'title_link', 'description', 'image',
    'type', 'style', 'status', 'words_count',
    'release_date', 'work_points',
]
AUTHOR_FIELDS = [
    'author_name', 'author_description', 'author_note', 'autor_image',
]


async def get_author_page_data(page: Page, blocks: dict, **kwargs):
    blocks = {key: val['selector'] for key, val in blocks.items()}
    data = {}
    data['author_data'] = await get_data_by_fields(
        page, blocks, kwargs['url'], AUTHOR_FIELDS, single=True
    )
    data['title_data'] = split_by_fields(await get_data_by_fields(
        page, blocks, kwargs['url'], TITLE_FIELDS
    ))
    data.update(get_additional_info(**kwargs))
    return data
