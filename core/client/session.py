# coding=utf-8
"""
封装获取 cookie 方法
"""
import requests
from core.config.settings import config
from core.utils.logger import get_log
from core.utils.yaml_helper import Yaml


class Session:
    def __init__(self):
        self.config = config

    @staticmethod
    def get_session(env):
        """
        获取 qq 登陆 session
        获取 mobile+password 登录 session
        :param env: 环境
        :return: 登陆 token
        """
        if env == "banban-release":
            try:
                headers = Yaml.read_yaml('basic.yml', 'header_release')
                params = Yaml.read_yaml('basic.yml', 'params_qq')
                login_url = config.qq_login_url + '?' + params + '&package=sg.ola.party.alo'  # 7.22 修改，请求接口加包名限制
                body = Yaml.read_yaml('basic.yml', 'data_qq')
                session = requests.session()
                res = session.post(login_url, data=body, headers=headers, verify=False)
                res.raise_for_status()
                res = res.json()
                print(res)
                tokenDict = {'token': res['data'].get('token'), 'uid': res['data']['uid']}
                return tokenDict['token']
            except Exception as error:
                get_log('getSession.log').error(f'session 异常，原因：{error}')
        elif env == "dev":
            try:
                headers = Yaml.read_yaml('basic.yml', 'header_dev')
                params = Yaml.read_yaml('basic.yml', 'params_dev_qq')
                login_url = config.qq_login_url + '?' + params + '&package=com.imbb.banban.android'  # 7.22 修改，请求接口加包名限制
                body = Yaml.read_yaml('Basic.yml', 'data_dev_qq')
                session = requests.session()
                res = session.post(login_url, data=body, headers=headers, verify=False)
                res.raise_for_status()
                res = res.json()
                print(f'使用默认方案：token:{res["data"].get("token")}')
                tokenDict = {'token': res['data'].get('token'), 'uid': res['data']['uid']}
                return tokenDict['token']
            except Exception as error:
                get_log('getSession.log').error(f'默认方案 session 异常，原因：{error}')

        else:
            print("env input error")
