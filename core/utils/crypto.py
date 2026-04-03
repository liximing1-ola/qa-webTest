"""
加密和签名工具模块
"""
import hashlib
from urllib.parse import urlencode
from core.config.settings import config
from core.utils.logger import get_log
import json

logger = get_log('crypto.log')


def hash_md5(text):
    """
    计算字符串的 MD5 哈希值
    
    支持中文和英文字符
    
    :param text: 输入文本
    :return: MD5 哈希值（十六进制字符串）
    """
    try:
        # 使用 UTF-8 编码处理中文和英文
        return hashlib.md5(text.encode(encoding='utf-8')).hexdigest()
    except Exception as e:
        logger.error(f'MD5 计算失败: {str(e)}')
        raise


def hash_sign(url_query, url_format='json', **kwargs):
    """
    生成签名字符串用于 API 请求
    
    签名算法：
    1. 按字母顺序排序查询参数
    2. 拼接参数为 "key1=value1&key2=value2" 的形式
    3. 添加密钥后缀 "!rilegoule#"
    4. 计算 MD5 哈希
    
    :param url_query: 查询参数字典
    :param url_format: 响应格式（'json' 或 'pb'）
    :param kwargs: 额外参数（如 ver, uid 等）
    :return: URL 编码的查询字符串
    """
    try:
        # 复制查询参数，避免修改原字典
        query_params = url_query.copy()

        # 设置格式
        query_params['format'] = 'json' if url_format == 'json' else 'pb'

        # 构建签名内容：按键排序，拼接参数
        sign_parts = []
        for key in sorted(query_params.keys()):
            value = query_params[key]
            if value is not None:
                sign_parts.append(f'{key}={value}')

        # 添加签名密钥
        sign_content = '&'.join(sign_parts) + '!rilegoule#'

        # 计算签名
        query_params['_sign'] = hashlib.md5(
            sign_content.encode(encoding='utf-8')
        ).hexdigest()

        # 添加额外参数
        query_params.update(kwargs)

        logger.debug(f'签名生成成功 (格式: {url_format})')
        return urlencode(query_params)

    except Exception as e:
        logger.error(f'签名生成失败: {str(e)}')
        raise


def add_url(url_host, url_base, url_query, url_format='json', **kwargs):
    """
    构建完整的 API 请求 URL
    
    :param url_host: API 主机地址（如 https://api.example.com）
    :param url_base: 请求路径（如 /rank/charmAchieve）
    :param url_query: 查询参数字典
    :param url_format: 响应格式（'json' 或 'pb'）
    :param kwargs: 额外参数
    :return: 完整的 URL
    """
    try:
        # 构建 URI
        uri = url_host + url_base

        # 确保路径以 / 结尾
        if not uri.endswith('/'):
            uri += '/'

        # 生成签名查询字符串
        query_string = hash_sign(url_query, url_format, **kwargs)

        # 组合成完整 URL
        full_url = uri + '?' + query_string

        logger.debug(f'URL 构建成功: {url_base}')
        return full_url

    except Exception as e:
        logger.error(f'URL 构建失败: {str(e)}')
        raise


if __name__ == '__main__':
    # 测试示例
    from core.client.request import get_request_session

    # 构建测试 URL
    test_url = add_url(
        'https://api.sleeplessplanet.com',
        '/go/slp/gift/panel',
        config.banban_query,
        'json',
        ver=15,
        uid=200000089
    )
    print(f'生成的 URL: {test_url}')

    # 发送测试请求
    try:
        response = get_request_session(test_url, data=None)
        print(f'响应: {json.dumps(response, indent=2, ensure_ascii=False)}')
    except Exception as e:
        print(f'请求失败: {str(e)}')
