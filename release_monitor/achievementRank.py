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
def achievementRank(rankType, tab=1):
    if rankType == 1:
        incomeRank = ''
        incomeTotal_50 = 0
        incomeTotal_100 = 0
        time_total = '本日'
        user_profile_url = add_url(url_host=config.release_bb_host,
                                   url_base='rank/charmAchieve',
                                   url_query=config.banban_query,
                                   url_format='json',
                                   type=rankType,
                                   tab=tab,
                                   page=1)
        res = Request.get_request_session(url=user_profile_url, data=None)
        if tab == 2:
            time_total = '本周'
        for i in res['body']['data']['list'][:10]:
            incomeRank += ('{} | {} - {}收入:{}\n'.format(i['uid'], i['name'], time_total, i['score']))
        for j in res['body']['data']['list']:
            incomeTotal_50 += int(j['score'])
        user_profile_url = add_url(url_host=config.release_bb_host,
                                   url_base='rank/charmAchieve',
                                   url_query=config.banban_query,
                                   url_format='json',
                                   type=rankType,
                                   tab=tab,
                                   page=2)
        print(user_profile_url)
        res = Request.get_request_session(url=user_profile_url, data=None)
        for j in res['body']['data']['list']:
            incomeTotal_100 += int(j['score'])
        incomeRank += '截止{} 前100用户{}收入总额：{}元'.format(strftime('%m-%d %H:%M', localtime(time())),
                                                               time_total,
                                                             (incomeTotal_50 + incomeTotal_100))
        print(incomeRank)
        robot('success', incomeRank)

    if rankType == 2:
        payRank = ''
        payTotal_50 = 0
        payTotal_100 = 0
        time_total = '本日'
        user_profile_url = add_url(url_host=config.release_bb_host,
                                   url_base='rank/charmAchieve',
                                   url_query=config.banban_query,
                                   url_format='json',
                                   type=rankType,
                                   tab=tab,
                                   page=1)
        res = Request.get_request_session(url=user_profile_url, data=None)
        if tab == 2:
            time_total = '本周'
        for i in res['body']['data']['list'][:10]:
            payRank += ('{} | {} - {}消费:{}\n'.format(i['uid'], i['name'], time_total, i['score']))
        for j in res['body']['data']['list']:
            payTotal_50 += int(j['score'])
        user_profile_url = add_url(url_host=config.release_bb_host,
                                   url_base='rank/charmAchieve',
                                   url_query=config.banban_query,
                                   url_format='json',
                                   type=rankType,
                                   tab=tab,
                                   page=2)
        res = Request.get_request_session(url=user_profile_url, data=None)
        for j in res['body']['data']['list']:
            payTotal_100 += int(j['score'])
        payRank += '截止{} 前100用户{}消费总额：{}元'.format(strftime('%m-%d %H:%M', localtime(time())),
                                                            time_total,
                                                         payTotal_50 + payTotal_100)
        print(payRank)
        robot('success', payRank)


if __name__ == '__main__':
    achievementRank(1, 1)
    achievementRank(2, 1)
