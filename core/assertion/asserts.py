"""
封装 assert 方法
"""
import json
from core.utils.logger import get_log
from core import Consts


def assert_code(code, expected_code):
    """
    验证 response 状态码
    :param code:
    :param expected_code:
    :return:
    """
    try:
        assert code == expected_code
        return True
    except:
        get_log('assert.log').error(f"statusCode error, expected_code is {expected_code}, statusCode is {code}")
        Consts.RESULT_LIST.append('fail')
        raise


def assert_body(body, body_msg, expected_msg):
    """
    验证 response body 中任意属性的值
    :param body:
    :param body_msg:
    :param expected_msg:
    :return:
    """
    try:
        msg = body[body_msg]
        assert msg == expected_msg
        return True
    except:
        get_log('assert.log').error(f"Response body msg != expected_msg, expected_msg is {expected_msg}, body_msg is {body_msg}")
        Consts.RESULT_LIST.append('fail')
        raise


def assert_in_text(body, expected_msg):
    """
    验证 response body 中是否包含预期字符串
    :param body:
    :param expected_msg:
    :return:
    """
    try:
        text = json.dumps(body, ensure_ascii=False)
        assert expected_msg in text
        return True
    except:
        get_log('assert.log').error(f"Response body Does not contain expected_msg, expected_msg is {expected_msg}")
        Consts.RESULT_LIST.append('fail')
        raise


def assert_text(body, expected_msg):
    """
    验证 response body 中是否等于预期字符串
    :param body:
    :param expected_msg:
    :return:
    """
    try:
        assert body == expected_msg
        return True
    except:
        get_log('assert.log').error(f"Response body != expected_msg, expected_msg is {expected_msg}, body is {body}")
        Consts.RESULT_LIST.append('fail')
        raise


def assert_time(time, expected_time):
    """
    验证 response body 响应时间小于预期最大响应时间，单位：毫秒
    :param time:
    :param expected_time:
    :return:
    """
    try:
        assert time < expected_time
        return True
    except:
        get_log('assert.log').error(f"Response time > expected_time, expected_time is {expected_time}, time is {time}")
        Consts.RESULT_LIST.append('fail')
        raise


def assert_len(body, body_msg, expected_len):
    """
    验证 response body 中任意属性的值
    :param expected_len:
    :param body:
    :param body_msg:
    :return:
    """
    try:
        data = body[body_msg]
        assert len(data) >= expected_len
        return True
    except:
        get_log('assert.log').error("Response body len")
        Consts.RESULT_LIST.append('fail')
        raise
