import aiohttp
import asyncio

URL = ('https://translate.googleapis.com/translate_a/single?client=gtx&sl='
       '{src}&tl={dst}&dt=t&q={text}&ie=UTF-8&oe=UTF-8')


async def make_request(session, url, headers):
    async with session.get(url, headers=headers) as resp:
        try:
            json_data = await resp.json()
            # print(url)
            return ''.join([x[0] for x in json_data[0]])
        except Exception as e:
            # print(resp)
            return e


async def get_translate(data, src, dst):
    async with aiohttp.ClientSession() as session:
        headers = {
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
        url = URL.format(src=src, dst=dst, text=' ||| '.join(data))
        res = await make_request(session, url, headers)
        return res.split(' ||| ') if isinstance(res, str) else res



if __name__ == '__main__':
    data = ["她从自己身上破破烂烂的衣服!", "她从自己身上破破烂烂的衣服...", "她从自己身上破破烂烂的衣服!", "她从自己身上破破烂烂的衣服..."]
    src = 'auto'
    dst = 'ru'
    result = asyncio.run(get_translate(data, src, dst))
    print(result)
