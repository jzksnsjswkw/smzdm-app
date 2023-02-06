import hashlib
import random
import time
import requests


key = 'apr1$AwP!wRRT$gJ/q.X24poeBInlUJC'
user_tuple = (
    {
        'sk': '',
        'token': '',
        'cookie': r'',
    },
)


def md5(m: str):
    return hashlib.md5(m.encode()).hexdigest()


def sign(sk: str, token: str, cookie: str):
    url = 'https://user-api.smzdm.com/checkin'
    timestamp = int(time.time())
    headers = {
        'user-agent': 'smzdm_android_V10.4.20 rv:860 (Redmi Note 3;Android10;zh)smzdmapp',
        'request_key': str(
            random.randint(10000000, 100000000) * 10000000000 + timestamp
        ),
        'cookie': cookie,
        'content-type': 'application/x-www-form-urlencoded',
    }
    timestamp = timestamp - random.randint(0, 10)
    data = {
        'weixin': '1',
        'captcha': '',
        'f': 'android',
        'v': '10.4.20',
        'sk': sk,
        'sign': md5(
            f'f=android&sk={sk}&time={timestamp*1000}&token={token}&v=10.4.20&weixin=1&key={key}'
        ).upper(),
        'touchstone_event': '',
        'time': timestamp * 1000,
        'token': token,
    }
    return requests.post(url, headers=headers, data=data).json()


for user in user_tuple:
    print(sign(**user))
