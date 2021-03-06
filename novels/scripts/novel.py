import asyncio
from urllib.parse import urlparse, quote

from pyppeteer.page import Page
from pyppeteer.browser import Browser

from translate.scripts.pyppeteer_stealth import stealth
from translate.scripts.translate import get_browser
from novels.scripts import common
from novels.utils import get_string_format_keys
from utils.pyppeteer import intercept_resource, intercept_request_data
from utils.url import add_url_params, is_absolute
from utils.pyppeteer import get_pages_dict


async def set_interception_res(page: Page, res):
    # print(page._networkManager._userRequestInterceptionEnabled)
    await page.setRequestInterception(True)
    page.on('request', lambda req: asyncio.ensure_future(
        intercept_resource(req, res))
    )


async def set_interception_data(page: Page, search_data, search_param, url, **kwargs):
    await page.setRequestInterception(True)
    page.on('request', lambda req: asyncio.ensure_future(
        intercept_request_data(req, search_data, search_param, url, **kwargs))
    )


async def unset_interception(page: Page):
    await page.setRequestInterception(False)


async def get_page(
    browser, url: str, page_id,
    resourses_to_intercept=None, search_data=None, search_param=None
):
    pages = await browser.pages()
    pages = get_pages_dict(pages)
    try:
        page = pages[page_id]
    except IndexError:
        page = await browser.newPage()
    if search_data:
        kwargs = {'add_intercept': intercept_resource,
                  'type': resourses_to_intercept}
        await set_interception_data(
            page, search_data, search_param, url, **kwargs
        )
    elif resourses_to_intercept is not None:
        print(resourses_to_intercept)
        await set_interception_res(page, resourses_to_intercept)
    print(url)
    
    print('COMPLETE')
    return page


def get_page_url(**kwargs):

    # make params dict
    params = {}
    encoding = kwargs.get('encoding')
    if 'search_query_param' in kwargs and not kwargs['use_POST']:
        keywords = kwargs['keywords']
        keywords = quote(keywords, encoding=encoding) if encoding else keywords
        params[kwargs['search_query_param']] = keywords

    # add params to url
    url = kwargs['url']
    if not is_absolute(url):
        keys = get_string_format_keys(kwargs['urn'])
        format_data = {key: kwargs.get(key) for key in keys}
        url += kwargs['urn'].format(**format_data)
    if params:
        url = add_url_params(url, params)
    
    return url


async def get_resource_data(**kwargs):
    # prepare_browser_and_page
    # print(kwargs)
    browser = await get_browser(kwargs['browser_endpoint'])
    use_POST = kwargs.get('use_POST')
    url = get_page_url(**kwargs)

    page = await get_page(
        browser, url, kwargs['page_id'],
        resourses_to_intercept=kwargs['intercept_page_res'],
        search_data=kwargs.get('keywords') if use_POST else None,
        search_param=kwargs.get('search_query_param') if use_POST else None,
    )
    await stealth(page)
    await page.setViewport({'width': 1280, 'height': 720})
    await page.goto(url)

    
    return await getattr(common, f'get_{kwargs["name"]}_data')(
        page=page,
        **kwargs
    )
