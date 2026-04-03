"""
HTTP 请求客户端模块
"""

import requests
import urllib3
from core.utils.logger import get_log
from core.client.session import Session

urllib3.disable_warnings()

logger = get_log('request.log')


class ResponseWrapper:
    """响应包装类 - 标准化响应格式"""

    def __init__(self, status_code, body, time_consuming, time_total, error=None):
        self.code = status_code
        self.body = body
        self.time_consuming = time_consuming
        self.time_total = time_total
        self.error = error
        self.success = status_code == 200 and error is None

    def to_dict(self):
        """转换为字典格式"""
        return {
            'code': self.code,
            'body': self.body,
            'time_consuming': self.time_consuming,
            'time_total': self.time_total,
            'error': self.error,
            'success': self.success,
        }

    def __repr__(self):
        return f"ResponseWrapper(code={self.code}, success={self.success})"


def _normalize_url(url):
    """
    规范化 URL - 确保 URL 以 https:// 开头
    :param url: 输入的 URL
    :return: 规范化后的 URL
    """
    if not url.startswith(('http://', 'https://')):
        url = f'https://{url}'
        logger.warning(f'URL 已补充协议头: {url}')
    return url


def _build_headers(app_session='banban-release'):
    """
    构建请求头
    :param app_session: 应用 session 类型
    :return: 请求头字典
    """
    token = Session.get_session(app_session)
    return {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "user-token": token,
    }


def _extract_response_data(response):
    """
    提取响应数据
    :param response: 响应对象
    :return: 响应体和错误信息
    """
    try:
        body = response.json()
        return body, None
    except ValueError as e:
        error_msg = f'JSON 解析失败: {str(e)}'
        logger.error(error_msg)
        return response.text, error_msg
    except Exception as e:
        error_msg = f'响应提取失败: {str(e)}'
        logger.error(error_msg)
        return None, error_msg


def get_request_session(url, data=None, app_session='banban-release', timeout=30):
    """
    发送 GET 请求
    :param url: 请求 URL
    :param data: 查询参数（可选）
    :param app_session: 应用 session 类型（默认：banban-release）
    :param timeout: 超时时间（秒）
    :return: ResponseWrapper 对象或向后兼容的字典
    """
    # 规范化 URL
    url = _normalize_url(url)

    # 构建请求头
    headers = _build_headers(app_session)

    try:
        # 发送请求
        response = requests.get(
            url=url,
            params=data,
            headers=headers,
            timeout=timeout,
            verify=False  # 忽略 SSL 证书验证
        )
        response.raise_for_status()

        # 提取响应数据
        body, error = _extract_response_data(response)

        # 计算耗时
        time_consuming = response.elapsed.microseconds / 1000
        time_total = response.elapsed.total_seconds()

        # 创建响应包装
        wrapper = ResponseWrapper(
            status_code=response.status_code,
            body=body,
            time_consuming=time_consuming,
            time_total=time_total,
            error=error
        )

        logger.info(f'请求成功: {url} ({time_total:.2f}s)')
        return wrapper.to_dict()

    except requests.exceptions.Timeout:
        error_msg = f'请求超时: {url}'
        logger.error(error_msg)
        wrapper = ResponseWrapper(
            status_code=0,
            body=None,
            time_consuming=0,
            time_total=timeout,
            error=error_msg
        )
        return wrapper.to_dict()

    except requests.exceptions.ConnectionError as e:
        error_msg = f'连接错误: {url} - {str(e)}'
        logger.error(error_msg)
        wrapper = ResponseWrapper(
            status_code=0,
            body=None,
            time_consuming=0,
            time_total=0,
            error=error_msg
        )
        return wrapper.to_dict()

    except requests.RequestException as e:
        error_msg = f'请求异常: {url} - {str(e)}'
        logger.error(error_msg)
        wrapper = ResponseWrapper(
            status_code=0,
            body=None,
            time_consuming=0,
            time_total=0,
            error=error_msg
        )
        return wrapper.to_dict()

    except Exception as e:
        error_msg = f'未知错误: {url} - {str(e)}'
        logger.error(error_msg)
        wrapper = ResponseWrapper(
            status_code=0,
            body=None,
            time_consuming=0,
            time_total=0,
            error=error_msg
        )
        return wrapper.to_dict()
