"""
封装加密方法
"""
import hashlib
from urllib.parse import urlencode
from common.Request import get_request_session
from common.Config import config
import json


# MD5加密
def hash_md5(ch):
    for i in ch:
        if u'\u4e00' <= i <= u'\u9fff':
            return hashlib.md5(ch.encode(encoding='utf-8')).hexdigest()
        else:
            m = hashlib.md5()
            b = ch.encode(encoding='utf-8')
            m.update(b)
            return m.hexdigest()


def hash_sign(url_query, url_format, **kwargs):
    if url_format == 'json':
        url_query['format'] = 'json'
    else:
        url_query['format'] = 'pb'

    hashArgs = []
    for key in sorted(url_query.keys()):
        if url_query[key] is not None:
            hashArgs.append(f'{key}={url_query[key]}')

    content = '&'.join(hashArgs) + '!rilegoule#'
    url_query['_sign'] = hashlib.md5(bytes(content, encoding='utf-8')).hexdigest()

    for key, value in kwargs.items():
        url_query[key] = value
    return urlencode(url_query)


def add_url(url_host, url_base, url_query, url_format, **kwargs):
    uri = url_host + url_base
    if not uri.endswith('/'):
        uri += '/'
    return uri + '?' + hash_sign(url_query, url_format, **kwargs)


if __name__ == '__main__':
    url = add_url(config.release_bb_host, 'go/banban/profile/home/', config.banban_query, 'json', ver=3, uid=100291520)
    print(url)
    re = get_request_session(url, data=None)
    print(re)
    print(json.dumps(re))
    print(re['body']['data']['base']['name'])

