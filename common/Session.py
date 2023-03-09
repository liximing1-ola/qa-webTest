# coding=utf-8
"""
封装获取cookie方法
"""
import requests
from common.Config import config
from common import Logs
from common.Yaml import Yaml


class Session:
    def __init__(self):
        self.config = config

    @staticmethod
    def get_session(env):
        """
        获取qq登陆session
        获取mobile+password登录session
        :param env: 环境
        :return: 登陆token
        """
        if env == "banban-release":
            try:
                headers = Yaml.read_yaml('basic.yml', 'header_release')
                params = Yaml.read_yaml('basic.yml', 'params_qq')
                login_url = config.qq_login_url + '?' + params + '&package=com.imbb.banban.android'  # 7.22修改，请求接口加包名限制
                body = Yaml.read_yaml('basic.yml', 'data_qq')
                session = requests.session()
                res = session.post(login_url, data=body, headers=headers, verify=False)
                res.raise_for_status()
                res = res.json()
                tokenDict = {'token': res['data'].get('token'), 'uid': res['data']['uid']}
                return tokenDict['token']
            except Exception as error:
                Logs.get_log('getSession.log').error('session异常，原因： {}'.format(error))
        elif env == "dev":
            try:
                headers = Yaml.read_yaml('basic.yml', 'header_dev')
                params = Yaml.read_yaml('basic.yml', 'params_dev_qq')
                login_url = config.qq_login_url + '?' + params + '&package=com.imbb.banban.android'  # 7.22修改，请求接口加包名限制
                body = Yaml.read_yaml('Basic.yml', 'data_dev_qq')
                session = requests.session()
                res = session.post(login_url, data=body, headers=headers, verify=False)
                res.raise_for_status()
                res = res.json()
                print('使用默认方案：token:{}'.format(res['data'].get('token')))
                tokenDict = {'token': res['data'].get('token'), 'uid': res['data']['uid']}
                return tokenDict['token']
            except Exception as error:
                Logs.get_log('getSession.log').error('默认方案session异常，原因： {}'.format(error))

        else:
            print("env input error")
