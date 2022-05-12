import json

import requests
from django.core.management.base import BaseCommand
from pyquery import PyQuery as pq

from parsers.models import Language, Parser
from utils.browser import *
from parsers.scripts.translate import get_browser as get_browser_inst
from parsers.scripts.translate import get_page as get_page_inst
from parsers.api.serializers import ParserSerializer


SERVICES = {
    'google': {
        'src': 'div.aCQag > c-wiz > div:nth-child(2) > c-wiz > div.OoYv6d > div > div.dykxn.MeCBDd.j33Gae > div > div:nth-child(3) > div[data-language-code="{code}"]',
        'dst': 'div.aCQag > c-wiz > div:nth-child(2) > c-wiz > div.ykTHSe > div > div.dykxn.MeCBDd.j33Gae > div > div:nth-child(2) > div[data-language-code="{code}"]',
        'auto': 'div.aCQag > c-wiz > div:nth-child(2) > c-wiz > div.OoYv6d > div > div.dykxn.MeCBDd.j33Gae > div > div:nth-child(1) > div[data-language-code="auto"]',
    },
    'deepl': {
        'src': 'button[dl-test=translator-lang-option-{code}]',
        'dst': 'button[dl-test=translator-lang-option-{code}-{code_upper}]',
        'auto': 'button[dl-test=translator-lang-option-auto]',
    },
    'yandex': {
        'src': 'div[data-value={code}]',
        'dst': 'div[data-value={code}]',
        'auto': '',
    },
}


def translate_into_en(langs):
    url = 'http://127.0.0.1:8000/api/parsers/translate/deepl'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'paragraphs': langs,
        'src': 'auto',
        'dst': 'en'
    }
    r = requests.post(
        url=url,
        headers=headers,
        data=json.dumps(data),
    )
    return [x.title() for x in r.json()]


async def get_page_content(endpoint, url, page_index, blocks):
    browser = await get_browser_inst(endpoint)
    page = await get_page_inst(browser, url, page_index)
    await page.setViewport({'width': 1280, 'height': 720})
    await page.screenshot({'path': 'update_langs.png'})
    await page.click(blocks['source_button'], delay=200)
    return await page.content()


def get_blocks_data(service_name):
    parser = Parser.objects.annotate_related_parser_slug().filter(
        related_parser_slug=service_name
    ).first()
    parser_data = ParserSerializer(instance=parser).data
    return parser_data['blocks']


def fill_langs_data(service_name, langs_data):
    parser = Parser.objects.annotate_related_parser_slug().filter(
        related_parser_slug=service_name
    ).first()
    langs_data.append({
        'parser': parser,
        'name': 'Auto',
        'code': 'auto',
        'source': SERVICES[service_name]['auto'],
    })
    for lang_data in langs_data:
        src = SERVICES[service_name]['src'].format(code=lang_data['code'])
        try:
            dst = SERVICES[service_name]['dst'].format(code=lang_data['code'])
        except KeyError:
            dst = SERVICES[service_name]['dst'].format(
                code=lang_data['code'],
                code_upper=lang_data['code'].upper(),
            )
        if lang_data['code'] != 'auto':
            lang_data.update({
                'source': src,
                'destination': dst,
                'parser': parser
            })
        Language.objects.update_or_create(**lang_data)


def handle_google(endpoint, url, page_index):
    src = SERVICES['google']['src']
    langs_selector = src[:src.rindex('>') + 2] + 'div[data-language-code]'
    content = asyncio.run(run_async2(
        get_page_content,
        endpoint=endpoint,
        url=url,
        page_index=page_index,
        blocks=get_blocks_data('google'),
    ))
    html = pq(content)
    codes = []
    langs = []
    for element in html(langs_selector):
        codes.append(element.attrib['data-language-code'])
        langs.append(element.cssselect('.Llmcnf')[0].text)
    tr_langs = translate_into_en(langs)
    langs_data = [{'code': k, 'name': v} for k, v in zip(codes, tr_langs)]
    fill_langs_data('google', langs_data)


def handle_yandex(endpoint, url, page_index):
    langs_selector = 'div.langs-item[data-value]'
    content = asyncio.run(run_async2(
        get_page_content,
        endpoint=endpoint,
        url=url,
        page_index=page_index,
        blocks=get_blocks_data('yandex'),
    ))
    html = pq(content)
    codes = []
    langs = []
    for element in html(langs_selector):
        codes.append(element.attrib['data-value'])
        langs.append(element.text.strip())
    tr_langs = translate_into_en(langs)
    langs_data = [{'code': k, 'name': v} for k, v in zip(codes, tr_langs)]
    fill_langs_data('yandex', langs_data)
    fill_langs_data('yandex-image', langs_data)


def handle_deepl(endpoint, url, page_index):
    langs_selector = 'button[dl-test^="translator-lang-option"]'
    content = asyncio.run(run_async2(
        get_page_content,
        endpoint=endpoint,
        url=url,
        page_index=page_index,
        blocks=get_blocks_data('deepl'),
    ))
    html = pq(content)
    codes = []
    langs = []
    for element in list(html(langs_selector))[1:]:
        codes.append(element.attrib['dl-test'].split('-')[-1])
        langs.append(element.cssselect('span')[0].text.strip())
    print(codes, langs)
    # tr_langs = translate_into_en(langs)
    # print(codes, langs)
    langs_data = [{'code': k, 'name': v} for k, v in zip(codes, langs)]
    # print(langs_data)
    fill_langs_data('deepl', langs_data)


class Command(BaseCommand):
    help = 'Update language data'

    def add_arguments(self, parser):
        parser.add_argument('--service', type=str)

    def get_handler(self, service_name):
        handlers = {
            'google': handle_google,
            'yandex': handle_yandex,
            'deepl': handle_deepl,
        }
        if service_name in handlers:
            return handlers[service_name]

    def handle(self, *args, **options):
        service = options.get('service') or 'all'
        services = SERVICES.keys() if service == 'all' else [service]
        browser = get_browser()
        # pages = []
        for service_name in services:
            page = get_page(service_name, browser)
            handler = self.get_handler(service_name)
            handler(browser.wsEndpoint, page.get_url(), page.index)
