import os
import time


class config:
    #  工程目录
    BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    #  生成报告结果地址
    results_path = os.path.join(BASE_PATH, 'Data/report/results')
    #  生成报告地址
    report_path = os.path.join(BASE_PATH, 'report')
    #  release域名
    domain_host = {'bb': 'https://api-new.yinjietd.com/',
                   'bb-46': 'https://192.168.11.46'}
    release_bb_host = domain_host['bb']

    # qq_login url
    qq_login_url = release_bb_host + 'account/qqlogin'

    banban_query = {'package': 'com.imbb.banban.android',
                    '_ipv': 0,
                    '_platform': 'android',
                    '_model': 'HD1900',
                    '_index': '666',
                    '_timestamp': int(time.time())}

