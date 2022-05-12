import requests
import json


def make_post_request(data, url):
    data = json.dumps(data)
    headers = {
        'Content-Type': 'application/json'
    }
    r = requests.post(url, data=data, headers=headers)
    return r.json()


if __name__ == '__main__':
    data = make_post_request(
        {'url': 'http://www.ywggzy.com/bxwx/26410/4033116_2.html'}, 
        'http://localhost:8000/api/novels/cn/ywggzy/from-url',
    )
    print(data)