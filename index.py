import hashlib
import operator
import random
import time

import requests

key = 'apr1$AwP!wRRT$gJ/q.X24poeBInlUJC'
user_tuple = (
    {
        'sk': '',
        'token': '',
        'cookie': '',
    },
)


def md5(m: str) -> str:
    return hashlib.md5(m.encode()).hexdigest()


def dict_to_query(a: list) -> str:
    query_str = ''
    for k, v in a:
        query_str += f"{k}={v}&"
    return query_str[:-1]


def get_sign(src: dict) -> str:
    data = src.copy()
    if 'sign' in data:
        del data['sign']

    # del key if value is ''
    for k in list(data.keys()):
        if not data[k]:
            del data[k]

    sorted_data = sorted(data.items(), key=operator.itemgetter(0))
    m = dict_to_query(sorted_data) + f'&key={key}'
    return md5(m).upper()


def get_headers_and_timestamp_wrapper():
    timestamp = (int(time.time()) - random.randint(10, 20)) * 1000

    def get_headers_and_timestamp(cookie: str):
        headers = {
            'User-Agent': 'smzdm_android_V10.4.26 rv:866 (Redmi Note 3;Android10;zh)smzdmapp',
            'request_key': str(
                random.randint(10000000, 100000000) * 10000000000 + int(time.time())
            ),
            'Cookie': cookie,
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        return headers, timestamp

    return get_headers_and_timestamp


get_headers_and_timestamp = get_headers_and_timestamp_wrapper()


def checkin(sk: str, token: str, cookie: str) -> bool:
    url = 'https://user-api.smzdm.com/checkin'
    headers, timestamp = get_headers_and_timestamp(cookie)
    timestamp = int(time.time())
    data = {
        'weixin': '1',
        'captcha': '',
        'f': 'android',
        'v': '10.4.26',
        'sk': sk,
        'touchstone_event': '',
        'time': timestamp,
        'token': token,
    }
    data['sign'] = get_sign(data)
    res = requests.post(url, headers=headers, data=data).json()
    print('checkin --->', res)
    if res['error_code'] != '0':
        raise Exception(res['error_msg'])

    if '成功' in res['error_msg']:
        return True
    else:
        return False


def reward(url: str, cookie: str) -> bool:
    headers, timestamp = get_headers_and_timestamp(cookie)
    data = {
        'weixin': '1',
        'time': timestamp,
        'basic_v': '0',
        'f': 'android',
        'v': '10.4.26',
    }
    data['sign'] = get_sign(data)
    res = requests.post(url, headers=headers, data=data).json()
    print(url.split('/')[-1], '--->', res)

    if res['error_code'] == '0':
        return True
    if res['error_code'] == '4':
        return False
    else:
        raise Exception(res['error_msg'])


def all_reward(cookie: str) -> bool:
    url = 'https://user-api.smzdm.com/checkin/all_reward'
    return reward(url, cookie)


def extra_reward(cookie: str) -> bool:
    url = 'https://user-api.smzdm.com/checkin/extra_reward'
    return reward(url, cookie)


for user in user_tuple:
    print(checkin(**user))
    print(all_reward(user['cookie']))
    print(extra_reward(user['cookie']))
