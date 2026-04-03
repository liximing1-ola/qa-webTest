"""
成就排行监控模块 - 用于监控用户收入和消费排行
"""
from time import time, strftime, localtime
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from core.config.settings import config
from core.client import Request
from core.utils.crypto import add_url
from libs.robot import robot


class RankMonitor:
    """排行监控类"""

    # 排行类型定义
    RANK_TYPES = {
        1: {'name': '收入', 'key': 'incomeRank', 'metric': '收入'},
        2: {'name': '消费', 'key': 'payRank', 'metric': '消费'},
    }

    # 时间周期定义
    TIME_PERIODS = {
        1: {'name': '本日', 'api_value': 1},
        2: {'name': '本周', 'api_value': 2},
    }

    @staticmethod
    def _fetch_rank_data(rank_type, tab, page):
        """
        获取排行数据
        :param rank_type: 排行类型（1=收入, 2=消费）
        :param tab: 时间周期（1=本日, 2=本周）
        :param page: 页码
        :return: 排行数据列表
        """
        url = add_url(
            url_host=config.release_bb_host,
            url_base='rank/charmAchieve',
            url_query=config.banban_query,
            url_format='json',
            type=rank_type,
            tab=tab,
            page=page
        )
        res = Request.get_request_session(url=url, data=None)
        
        if res['code'] != 200:
            raise Exception(f"API 返回错误: {res['code']}")
        
        return res['body']['data']['list']

    @staticmethod
    def _format_rank_text(rank_data, time_period, metric, top_n=10):
        """
        格式化排行文本
        :param rank_data: 排行数据列表
        :param time_period: 时间周期名称
        :param metric: 指标名称（收入/消费）
        :param top_n: 显示的前N条
        :return: 格式化后的文本
        """
        text = ''
        for item in rank_data[:top_n]:
            text += f"{item['uid']} | {item['name']} - {time_period}{metric}:{item['score']}\n"
        return text

    @staticmethod
    def _calculate_total(rank_data):
        """
        计算总和
        :param rank_data: 排行数据列表
        :return: 总和
        """
        return sum(int(item['score']) for item in rank_data)

    @classmethod
    def get_achievement_rank(cls, rank_type, tab=1):
        """
        获取成就排行
        :param rank_type: 排行类型（1=收入, 2=消费）
        :param tab: 时间周期（1=本日, 2=本周）
        :return: 排行信息字符串
        """
        if rank_type not in cls.RANK_TYPES:
            raise ValueError(f"不支持的排行类型: {rank_type}")

        if tab not in cls.TIME_PERIODS:
            raise ValueError(f"不支持的时间周期: {tab}")

        rank_info = cls.RANK_TYPES[rank_type]
        time_period = cls.TIME_PERIODS[tab]['name']

        try:
            # 获取第一页数据（前50名）
            rank_data_1 = cls._fetch_rank_data(rank_type, tab, 1)
            total_50 = cls._calculate_total(rank_data_1)
            rank_text = cls._format_rank_text(rank_data_1, time_period, rank_info['metric'])

            # 获取第二页数据（51-100名）
            rank_data_2 = cls._fetch_rank_data(rank_type, tab, 2)
            total_100 = cls._calculate_total(rank_data_2)

            # 组合成果
            total = total_50 + total_100
            timestamp = strftime('%m-%d %H:%M', localtime(time()))

            rank_text += f"截止{timestamp} 前 100 用户{time_period}{rank_info['metric']}总额：{total}元"

            return rank_text

        except Exception as e:
            error_msg = f"获取{rank_info['name']}排行失败: {str(e)}"
            print(error_msg)
            return error_msg


def achievementRank(rankType, tab=1):
    """
    获取成就排行（兼容旧接口）
    :param rankType: 排行类型（1=收入, 2=消费）
    :param tab: 时间周期（1=本日, 2=本周）
    """
    try:
        rank_text = RankMonitor.get_achievement_rank(rankType, tab)
        print(rank_text)
        robot('success', rank_text)
    except Exception as e:
        print(f"错误: {str(e)}")
        robot('fail', str(e), title='achievementRank')


if __name__ == '__main__':
    # 获取收入排行
    achievementRank(1, 1)
    
    # 获取消费排行
    achievementRank(2, 1)
