import pytest
# import allure
from common.Config import config
from common import Request, Assert
from common.Json import Json
from common.Yaml import Yaml
from common.Hash import add_url


class TestUserInfo(object):

    # @allure.title('Verify interface data')
    # @allure.description('检查接口状态')
    def test_01_UserProfileHome(self):
        """
        用例描述：
        """
        user_profile_url = add_url(url_host=config.release_bb_host,
                                   url_base='go/banban/profile/home',
                                   url_query=config.banban_query,
                                   url_format='json',
                                   ver=3,
                                   uid=126425689)
        res = Request.get_request_session(url=user_profile_url, data=None)
        Assert.assert_code(res['code'], 200)
        Assert.assert_body(res['body'], 'success', 1)
        Assert.assert_len(res['body'], 'data', 1)
        print(res['body']['data'])


if __name__ == '__main__':
    userInfo = TestUserInfo.test_01_UserProfileHome
