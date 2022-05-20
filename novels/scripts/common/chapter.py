import re

from pyppeteer.page import Page
from django.urls import reverse
from requests import get

from utils.pyppeteer import get_elements_attr
from utils.url import is_absolute, join_url
from utils.request import make_post_request
from novels.utils import get_additional_info, get_data_by_fields, get_links_data


CHAPTER_FIELDS = [
    'author_note', 'text', 'name'
]
NAVIGATION_LINKS = {
    'next': 'next_chapter_link',
    'prev': 'prev_chapter_link',
}
CHAPTER_LINKS = [
    'author_link', 'title_link', 
]


async def get_chapter_text(page: Page, selector: str, exclude_tags) -> list:
    print(selector)
    await page.screenshot({'path': 'temp_imgs/pic.png'})
    return await page.evaluate(f'''
        (exclude_tags) => {{
            let ele = document.querySelector(`{selector}`);
            let text = ele.innerText;
            if (exclude_tags) {{
                for (var i = 0; i < ele.children.length; i++) {{
                    if (ele.children[i].tagName !== 'BR') {{
                        text = text.replace(ele.children[i].innerText, "");
                    }}
                }}
            }}
            return text.trim();
         }}
    ''', exclude_tags)


async def get_next_prev_links(page: Page, blocks, url):
    data = {}
    for key, val in NAVIGATION_LINKS.items():
        if val not in blocks:
            continue
        href = await get_elements_attr(page, blocks[val], 'href')
        if not href:
            continue
        data[key] = href[0] if is_absolute(href[0]) else join_url(url, href[0])
    return data


async def get_links(page: Page, blocks, url):
    data = {}
    data.update(await get_next_prev_links(page, blocks, url))
    data.update(await get_data_by_fields(
        page, blocks, url, CHAPTER_LINKS, single=True
    ))
    return data


async def get_full_chapter(data, **kwargs):
    link = data.get('next')
    if not link or not re.findall(r'(\d+)_(\d+).html', link):
        return data
    uri = kwargs['request'].build_absolute_uri(
        reverse('novels:execute_from_url', kwargs={
            'lang_code': kwargs['query_params']['lang_code'],
            'service': kwargs['query_params']['service'],
        })
    )
    resp_data = make_post_request({'url': link}, uri)
    data['text'] += '\n' + resp_data['text']
    data['next'] = resp_data['next']
    return data


async def get_chapter_page_data(page: Page, blocks: dict, **kwargs):
    data = {}
    for field in CHAPTER_FIELDS:
        if field not in blocks:
            continue
        data[field] = await get_chapter_text(
            page,
            blocks[field]['selector'],
            blocks[field]['exclude']
        )
    blocks = {key: val['selector'] for key, val in blocks.items()}
    data.update(await get_links(page, blocks, kwargs['url']))
    data = await get_full_chapter(data, **kwargs)
    data.update(get_additional_info(**kwargs))
    return data
