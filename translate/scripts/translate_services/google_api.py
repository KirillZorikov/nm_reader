import aiohttp
import asyncio

URL = ('https://translate.googleapis.com/translate_a/single?client=gtx&sl='
       '{src}&tl={dst}&dt=t&q={text}&ie=UTF-8&oe=UTF-8')
MAX_CHAR_PER_REQUEST = 700
DELIMITER = ' \n!!!\n '
HEADERS = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6,hy;q=0.5,eu;q=0.4',
    'Connection': 'keep-alive',
    'Referer': 'https://translate.googleapis.com/',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Mobile Safari/537.36',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
}


async def make_request(session, url, headers, data):
    async with session.get(url, headers=headers) as resp:
        json_data = await resp.json()
        trans = ''.join([x[0] for x in json_data[0]])
        trans_arr = trans.split(DELIMITER.strip())
        result = {key: '' for key in data}
        if len(data) != len(trans_arr):
            print(len(data), len(trans_arr))
            return result
        for i, parapraph in enumerate(data):
            result[parapraph] = trans_arr[i]
        return result


def chunks(arr):
    sub = []
    length = 0
    for element in arr:
        if len(element) + length < MAX_CHAR_PER_REQUEST:
            sub.append(element)
            length += len(element)
        else:
            yield sub
            length = len(element)
            sub = [element]
    else:
        yield sub


# def chunks(arr):
#     for x in arr:
#         yield [x]


async def get_translate(data, src, dst):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for chunk in chunks(set(data)):
            url = URL.format(src=src, dst=dst, text=DELIMITER.join(chunk))
            tasks.append(asyncio.ensure_future(
                make_request(session, url, HEADERS, chunk)))
        translates = await asyncio.gather(*tasks)
        result = {}
        for translate in translates:
            if len(translate) > 1 and all(val == '' for val in translate.values()):
                tasks = []
                for paragraph in translate:
                    url = URL.format(src=src, dst=dst, text=str(paragraph))
                    tasks.append(asyncio.ensure_future(
                        make_request(session, url, HEADERS, [paragraph])))
                paragraph_trans = await asyncio.gather(*tasks)
                for tran in paragraph_trans:
                    result.update(tran)
            else:
                result.update(translate)
        return result


if __name__ == '__main__':
    data = ["她从自己身上破破烂烂的衣服!", "她从自己身上破破烂烂的衣服...",
            "她从自己身上破破烂烂的衣服!", "她从自己身上破破烂烂的衣服..."]*50
    src = 'auto'
    dst = 'ru'
    result = asyncio.run(get_translate(data, src, dst))
    print(result)
