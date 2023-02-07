try:
    from time import time, strftime, localtime
    from common.Config import config
    from common import Request, Assert
    from common.Hash import add_url
    from common.Robot import robot
except EnvironmentError:
    import os
    import sys
    sys.path.append(os.path.split(os.path.abspath(os.path.dirname(__file__)))[0])


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
        for i in res['body']['data']['list']:
            payRank += ('{} | {} - 今日消费:{}\n'.format(i['uid'], i['name'], i['score']))
        payRank += '截止{} 用户消费前50（单位：元）'.format(strftime('%m-%d %H:%M', localtime(time())))
        print(payRank)
        robot('success', payRank)
    elif rankType == 1:
        incomeRank = ''
        for i in res['body']['data']['list']:
            incomeRank += ('{} | {} - 今日收入:{}\n'.format(i['uid'], i['name'], i['score']))
        incomeRank += '截止{} 用户收入前50（单位：元）'.format(strftime('%m-%d %H:%M', localtime(time())))
        print(incomeRank)
        robot('success', incomeRank)


if __name__ == '__main__':
    achievementRank(1)
    achievementRank(2)
