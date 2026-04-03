"""
项目配置管理模块

集中管理项目的所有配置参数
"""
import os
import time
from pathlib import Path


class Config:
    """项目全局配置类"""

    # ==================== 项目路径配置 ====================
    # 项目根目录（.../core/config/../..）
    BASE_PATH = str(Path(__file__).resolve().parents[2])

    # 数据目录
    DATA_PATH = os.path.join(BASE_PATH, 'data')

    # 日志目录
    LOG_PATH = os.path.join(DATA_PATH, 'logs')

    # 报告目录
    REPORT_PATH = os.path.join(DATA_PATH, 'reports')

    # 测试结果目录
    RESULTS_PATH = os.path.join(REPORT_PATH, 'results')

    # 配置文件目录
    CONFIG_PATH = os.path.join(BASE_PATH, 'config')

    # ==================== API 配置 ====================
    # API 域名配置
    DOMAIN_HOST = {
        'bb': 'https://api.sleeplessplanet.com/',
        'bb-46': 'https://192.168.11.46',
    }

    # Release 环境主机
    RELEASE_BB_HOST = DOMAIN_HOST['bb']

    # ==================== QQ 登录配置 ====================
    QQ_LOGIN_URL = RELEASE_BB_HOST + 'account/qqlogin'

    # ==================== 班班 API 查询参数 ====================
    BANBAN_QUERY = {
        'package': 'sg.ola.party.alo',
        '_ipv': 0,
        '_platform': 'ios',
        '_model': 'HD1900',
        '_index': '666',
        '_timestamp': int(time.time()),
    }

    # ==================== 向后兼容属性 ====================
    @property
    def results_path(self):
        """向后兼容：结果目录"""
        return self.RESULTS_PATH

    @property
    def report_path(self):
        """向后兼容：报告目录"""
        return self.REPORT_PATH

    @property
    def domain_host(self):
        """向后兼容：域名配置"""
        return self.DOMAIN_HOST

    @property
    def release_bb_host(self):
        """向后兼容：Release 主机"""
        return self.RELEASE_BB_HOST

    @property
    def qq_login_url(self):
        """向后兼容：QQ 登录 URL"""
        return self.QQ_LOGIN_URL

    @property
    def banban_query(self):
        """向后兼容：班班查询参数"""
        return self.BANBAN_QUERY

    @classmethod
    def ensure_directories(cls):
        """
        确保所有必需的目录都已创建
        """
        directories = [
            cls.DATA_PATH,
            cls.LOG_PATH,
            cls.REPORT_PATH,
            cls.RESULTS_PATH,
        ]

        for directory in directories:
            os.makedirs(directory, exist_ok=True)

    @classmethod
    def get_config(cls):
        """
        获取配置实例
        :return: Config 实例
        """
        instance = cls()
        instance.ensure_directories()
        return instance


# 全局配置实例
config = Config.get_config()


if __name__ == '__main__':
    # 测试配置
    print(f'项目根目录: {config.BASE_PATH}')
    print(f'日志目录: {config.LOG_PATH}')
    print(f'报告目录: {config.REPORT_PATH}')
    print(f'Release 主机: {config.RELEASE_BB_HOST}')
    print(f'QQ 登录 URL: {config.QQ_LOGIN_URL}')
    print(f'班班查询参数: {config.BANBAN_QUERY}')
