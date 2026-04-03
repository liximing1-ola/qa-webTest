from time import time, strftime, localtime
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from core.config.settings import config
from core.client import Request
from core.assertion import Assert
from core.utils.crypto import add_url
from libs.robot import robot


# 用户日收入消费榜单
def giftRank(rankType=1):
    """
    用例描述：
    """
    user_profile_url = add_url(url_host=config.release_bb_host,
                               url_base='rank/gift',
                               url_query=config.banban_query,
                               url_format='json',
                               type=rankType,
                               page=1)
    res = Request.get_request_session(url=user_profile_url, data=None)
    Assert.assert_code(res['code'], 200)
    Assert.assert_body(res['body'], 'success', 1)
    Assert.assert_len(res['body'], 'data', 1)
    # print(res['body']['data']['list'])
    if rankType == 2:
        payRank = ''
        for i in res['body']['data']['list']:
            payRank += ('{} | {} - 收到 {} {}个\n'.format(i['uid'], i['user_name'], i['gift_name'],
                                                            i['gift_num']))
        print(payRank)
        # robot('success', payRank)
    elif rankType == 1:
        incomeRank = ''
        for i in res['body']['data']['list']:
            incomeRank += ('{} | {} - 送出 {} {}个\n'.format(i['uid'], i['user_name'], i['gift_name'],
                                                            i['gift_num']))

        print(incomeRank)
        # robot('success', incomeRank)


if __name__ == '__main__':
    giftRank(2)
    giftRank(1)
