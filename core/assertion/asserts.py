"""
API 响应断言模块

提供统一的断言方法，用于验证 API 响应的各项指标
"""
import json
from core.utils.logger import get_log
from core import Consts

logger = get_log('assert.log')


class AssertionError(Exception):
    """自定义断言错误异常"""
    pass


def _log_error_and_fail(error_msg):
    """
    记录错误日志并标记测试失败
    :param error_msg: 错误信息
    """
    logger.error(error_msg)
    Consts.RESULT_LIST.append('fail')
    raise AssertionError(error_msg)


def assert_code(code, expected_code):
    """
    验证响应状态码
    
    :param code: 实际状态码
    :param expected_code: 预期状态码
    :return: True 表示断言通过
    :raises: AssertionError 断言失败
    """
    try:
        if code != expected_code:
            error_msg = f'状态码不匹配: 期望 {expected_code}，实际 {code}'
            _log_error_and_fail(error_msg)
        logger.debug(f'✓ 状态码验证通过: {code}')
        return True
    except AssertionError:
        raise
    except Exception as e:
        error_msg = f'状态码验证异常: {str(e)}'
        _log_error_and_fail(error_msg)


def assert_body(body, body_key, expected_value):
    """
    验证响应体中指定字段的值
    
    :param body: 响应体（字典）
    :param body_key: 要验证的字段键
    :param expected_value: 期望值
    :return: True 表示断言通过
    :raises: AssertionError 断言失败
    """
    try:
        if body_key not in body:
            error_msg = f'响应体中不存在字段: {body_key}'
            _log_error_and_fail(error_msg)

        actual_value = body[body_key]
        if actual_value != expected_value:
            error_msg = f'字段 {body_key} 值不匹配: 期望 {expected_value}，实际 {actual_value}'
            _log_error_and_fail(error_msg)

        logger.debug(f'✓ 字段验证通过: {body_key} = {actual_value}')
        return True
    except AssertionError:
        raise
    except Exception as e:
        error_msg = f'字段验证异常: {str(e)}'
        _log_error_and_fail(error_msg)


def assert_in_text(body, expected_text):
    """
    验证响应体中是否包含指定的文本
    
    :param body: 响应体（可以是字典、列表或字符串）
    :param expected_text: 期望包含的文本
    :return: True 表示断言通过
    :raises: AssertionError 断言失败
    """
    try:
        # 将响应体转换为 JSON 字符串
        body_text = json.dumps(body, ensure_ascii=False) if not isinstance(body, str) else body

        if expected_text not in body_text:
            error_msg = f'响应体不包含期望文本: {expected_text}'
            _log_error_and_fail(error_msg)

        logger.debug(f'✓ 文本包含验证通过: 包含 "{expected_text}"')
        return True
    except AssertionError:
        raise
    except Exception as e:
        error_msg = f'文本验证异常: {str(e)}'
        _log_error_and_fail(error_msg)


def assert_text(body, expected_text):
    """
    验证响应体是否完全等于预期文本
    
    :param body: 响应体
    :param expected_text: 期望的完整文本
    :return: True 表示断言通过
    :raises: AssertionError 断言失败
    """
    try:
        if body != expected_text:
            error_msg = f'响应体不匹配: 期望 {expected_text}，实际 {body}'
            _log_error_and_fail(error_msg)

        logger.debug(f'✓ 响应体验证通过')
        return True
    except AssertionError:
        raise
    except Exception as e:
        error_msg = f'响应体验证异常: {str(e)}'
        _log_error_and_fail(error_msg)


def assert_time(actual_time, expected_max_time):
    """
    验证响应时间是否在预期范围内（毫秒）
    
    :param actual_time: 实际响应时间（毫秒）
    :param expected_max_time: 期望最大响应时间（毫秒）
    :return: True 表示断言通过
    :raises: AssertionError 断言失败
    """
    try:
        if actual_time >= expected_max_time:
            error_msg = f'响应时间超限: 期望 < {expected_max_time}ms，实际 {actual_time}ms'
            _log_error_and_fail(error_msg)

        logger.debug(f'✓ 响应时间验证通过: {actual_time}ms < {expected_max_time}ms')
        return True
    except AssertionError:
        raise
    except Exception as e:
        error_msg = f'响应时间验证异常: {str(e)}'
        _log_error_and_fail(error_msg)


def assert_len(body, body_key, expected_min_length):
    """
    验证响应体中指定字段的长度
    
    :param body: 响应体（字典）
    :param body_key: 要验证的字段键
    :param expected_min_length: 期望的最小长度
    :return: True 表示断言通过
    :raises: AssertionError 断言失败
    """
    try:
        if body_key not in body:
            error_msg = f'响应体中不存在字段: {body_key}'
            _log_error_and_fail(error_msg)

        data = body[body_key]
        actual_length = len(data)

        if actual_length < expected_min_length:
            error_msg = f'字段长度不符: 期望 >= {expected_min_length}，实际 {actual_length} (字段: {body_key})'
            _log_error_and_fail(error_msg)

        logger.debug(f'✓ 长度验证通过: {body_key} 长度 = {actual_length}')
        return True
    except AssertionError:
        raise
    except TypeError as e:
        error_msg = f'字段长度验证失败: 对象不支持 len() 操作 (字段: {body_key})'
        _log_error_and_fail(error_msg)
    except Exception as e:
        error_msg = f'长度验证异常: {str(e)}'
        _log_error_and_fail(error_msg)


# 向后兼容的别名
class Assert:
    """断言类 - 保持向后兼容性"""

    @staticmethod
    def assert_code(code, expected_code):
        """验证状态码"""
        return assert_code(code, expected_code)

    @staticmethod
    def assert_body(body, body_key, expected_value):
        """验证响应体字段"""
        return assert_body(body, body_key, expected_value)

    @staticmethod
    def assert_in_text(body, expected_text):
        """验证文本包含"""
        return assert_in_text(body, expected_text)

    @staticmethod
    def assert_text(body, expected_text):
        """验证完整文本"""
        return assert_text(body, expected_text)

    @staticmethod
    def assert_time(actual_time, expected_max_time):
        """验证响应时间"""
        return assert_time(actual_time, expected_max_time)

    @staticmethod
    def assert_len(body, body_key, expected_min_length):
        """验证长度"""
        return assert_len(body, body_key, expected_min_length)

