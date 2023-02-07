from time import time, strftime, localtime
import os
import sys

sys.path.append(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0])
from common.Config import config
from common import Request, Assert
from common.Hash import add_url
from common.Robot import robot


# if($op === 'consume' && (in_array($type,['chat-gift','defend','package','chat-coin','package-coin','coin-shop-buy','games-package']) || ($type === 'shop-buy' && in_array($reason['cid'], array(5, 6, 7)))))

# 用户日收入消费榜单
def achievementRank(rankType=1):
    """
    用例描述：
    """
    user_profile_url = add_url(url_host=config.release_bb_host,
                               url_base='rank/charmAchieve',
                               url_query=config.banban_query,
                               url_format='json',
                               type=rankType,
                               tab=1,
                               page=1)
    res = Request.get_request_session(url=user_profile_url, data=None)
    Assert.assert_code(res['code'], 200)
    Assert.assert_body(res['body'], 'success', 1)
    Assert.assert_len(res['body'], 'data', 1)
    if rankType == 2:
        payRank = ''
        payTotal = 0
        for i in res['body']['data']['list'][:10]:
            payRank += ('{} | {} - 今日消费:{}\n'.format(i['uid'], i['name'], i['score']))
        for j in res['body']['data']['list']:
            payTotal += int(j['score'])
        payRank += '截止{} 消费前50用户消费总额：{}元'.format(strftime('%m-%d %H:%M', localtime(time())),
                                                                    payTotal)
        print(payRank)
        robot('success', payRank)
    elif rankType == 1:
        incomeRank = ''
        incomeTotal = 0
        for i in res['body']['data']['list'][:10]:
            incomeRank += ('{} | {} - 今日收入:{}\n'.format(i['uid'], i['name'], i['score']))
        for j in res['body']['data']['list']:
            incomeTotal += int(j['score'])
        incomeRank += '截止{} 收入前50用户收入总额：{}元'.format(strftime('%m-%d %H:%M', localtime(time())),
                                                                incomeTotal)
        print(incomeRank)
        robot('success', incomeRank)


if __name__ == '__main__':
    achievementRank(1)
    achievementRank(2)
