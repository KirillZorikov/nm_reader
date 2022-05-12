import re

from pyppeteer.page import Page
from django.urls import reverse

from utils.pyppeteer import get_elements_attr
from utils.url import is_absolute, join_url
from utils.request import make_post_request


CHAPT_FIELDS = [
    'author_note', 'text'
]
NEXT_CHAP = 'next_chapter_link'


async def get_chapter_text(page: Page, selector: str, exclude_tags) -> list:
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


async def get_full_chapter(data, page: Page, selector, **kwargs):
    href = await get_elements_attr(page, selector, 'href')
    if not re.findall(r'(\d+)_(\d+)', href[0]):
        return data
    link = href[0] if is_absolute(href[0]) else join_url(kwargs['url'], href[0])
    uri = kwargs['request'].build_absolute_uri(
        reverse('novels:execute_from_url', kwargs={
            'lang_code': kwargs['query_params']['lang_code'], 
            'service': kwargs['query_params']['service'],
        })
    )
    resp_data = make_post_request({'url': link}, uri)
    data['text'] += '\n' + resp_data['text']
    return data
    

async def get_chapter_page_data(page: Page, blocks: dict, **kwargs):
    data = {}
    for field in CHAPT_FIELDS:
        if field not in blocks:
            continue
        data[field] = await get_chapter_text(
            page,
            blocks[field]['selector'],
            blocks[field]['exclude']
        )
    data = await get_full_chapter(data, page, blocks[NEXT_CHAP]['selector'], **kwargs)
    return data
