from pyppeteer.page import Page


from novels.utils import get_data_by_fields, split_by_fields


TITLE_FIELDS = [
    'author', 'title_link', 'description', 'image',
    'type', 'style', 'status', 'words_count',
    'release_date', 'work_points',
]
AUTHOR_FIELDS = [
    'author_name', 'author_description', 'author_note', 'autor_image',
]


# async def get_autor_text_data(page: Page, blocks):
#     data = {}
#     for field in AUTHOR_FIELDS:
#         if field in blocks:
#             data[field] = await get_elements_text(page, blocks[field])
#     return data


# async def get_autor_avatar_data(page: Page, blocks):
#     data = {}
#     if 'avatar' in blocks:
#         avatar_src = await get_elements_attr(page, blocks['avatar'], 'src')
#         data['avatar'] = avatar_src[0]
#     return data


# async def get_author_data(page: Page, blocks):
#     author_data = {}
#     author_data.update(await get_autor_avatar_data(page, blocks))
#     author_data.update(await get_autor_text_data(page, blocks))
#     return author_data


# async def get_title_data(page: Page, blocks, url):
#     title_data = {}
#     for field in TITLE_FIELDS:
#         if field not in blocks:
#             continue
#         if field.endswith('_link'):
#             title_data[field] = await get_links_data(page, blocks[field], url)
#         else:
#             title_data[field] = await get_elements_text(page, blocks[field])
#     return title_data


# async def get_links_data(page: Page, selector, url):
#     links_obj = await get_links_obj(page, selector)
#     links = []
#     for obj in links_obj:
#         href = obj['link']
#         obj['link'] = href if is_absolute(
#             href) else join_url(url, href)
#         obj['text'] = re.sub('\s+', ' ', obj['text'])
#         links.append(obj)
#     return links


# async def get_common_author_page_data(page: Page, blocks, url):
#     data = {}
#     data['author_data'] = await get_author_data(page, blocks)
#     data['title_data'] = await get_title_data(page, blocks, url)
#     data['title_data'] = split_by_fields(data['title_data'])
#     return data


async def get_author_page_data(page: Page, blocks: dict, **kwargs):
    blocks = {key: val['selector'] for key, val in blocks.items()}
    data= {}
    data['author_data'] = await get_data_by_fields(
        page, blocks, kwargs['url'], AUTHOR_FIELDS, single=True
    )
    data['title_data'] = split_by_fields(await get_data_by_fields(
        page, blocks, kwargs['url'], TITLE_FIELDS
    ))
    return data
