"""
封装 request
"""

import requests
import urllib3
from common import Logs
from common.Session import Session
urllib3.disable_warnings()


def get_request_session(url, data, app_session='banban-release'):
    """
    Get请求
    :param url:
    :param data:
    :param app_session:
    :return:
    """
    header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko)\
                          Chrome/67.0.3396.99 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "user-token": Session.get_session(app_session)
    }
    if not url.startswith('https://'):
        url = '%s%s' % ('https://', url)
        Logs.get_log('get_url.log').error('{} is error'.format(url))

    try:
        if data is None:
            response = requests.get(url=url, headers=header)
        else:
            response = requests.get(url=url, params=data, headers=header)

    except requests.RequestException as e:
        Logs.get_log('get_url.log').error('%s%s' % ('RequestException url: ', url))
        Logs.get_log('get_url.log').error(e)
        return ()
    except Exception as e:
        Logs.get_log('get_url.log').error('%s%s' % ('Exception url: ', url))
        Logs.get_log('get_url.log').error(e)
        return ()

    time_consuming = response.elapsed.microseconds / 1000
    time_total = response.elapsed.total_seconds()

    response_dicts = dict()
    response_dicts['code'] = response.status_code
    try:
        response_dicts['body'] = response.json()
    except Exception as e:
        Logs.get_log('get_url.log').error(e)
        response_dicts['body'] = ''
    # response_dicts['text'] = response.text
    response_dicts['time_consuming'] = time_consuming
    response_dicts['time_total'] = time_total

    return response_dicts
