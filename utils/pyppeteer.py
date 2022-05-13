from pyppeteer.page import Page

RESOURCE_TYPE = {
    'css': 'stylesheet',
    'img': 'image',
    'font': 'font',
    'fetch': 'fetch',
    'media': 'media',
    'js': 'script',
    '': 'blank',
}


async def intercept_resource(request, type):
    resources = set(RESOURCE_TYPE[x] for x in type.split('_'))
    if any(request.resourceType == _ for _ in resources):
        await request.respond({
            'status': 200,
            'body': 'foo'
        })
    elif request.isNavigationRequest() and len(request.redirectChain) != 0:
        await request.abort()
    else:
        await request.continue_()


async def intercept_request_data(
    request, req_data, req_param, url, add_intercept=None, **kwargs
):
    if request.url in url:
        headers = request.headers
        headers.update({
            'Content-Type': 'application/x-www-form-urlencoded'
        })
        data = {
            'method': 'POST',
            'postData': f'{req_param}={req_data}',
            'headers': headers,
        }
        return await request.continue_(data)
    if add_intercept:
        return await add_intercept(request, **kwargs)
    await request.continue_()


async def fill_input_value(page: Page, selector, value):
    await page.evaluate(f'''
            document.querySelector(`{selector}`).value = `{value}`;
        ''')


async def get_elements_text(page: Page, selector: str) -> list:
    return await page.evaluate(f'''
        () => [...document.querySelectorAll(`{selector}`)].map(element => element.innerText.trim())
    ''')


async def get_elements_attr(page: Page, selector: str, attr: str) -> list:
    return await page.evaluate(f'''
        () => [...document.querySelectorAll(`{selector}`)].map(element => element.getAttribute(`{attr}`))
    ''')
