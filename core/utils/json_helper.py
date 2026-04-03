"""
JSON 配置文件处理模块
参考: https://www.cnblogs.com/ChangAn223/p/11234348.html
"""
import json
import os
from pathlib import Path
from core.utils.logger import get_log
from core.config.settings import config
import jsonschema

logger = get_log('json.log')


class JsonFileNotFoundError(Exception):
    """JSON 文件不存在异常"""
    pass


class JsonValidationError(Exception):
    """JSON 校验失败异常"""
    pass


class JsonHelper:
    """JSON 文件读取和校验辅助类"""

    # 配置文件目录
    CONFIG_DIR = Path(config.BASE_PATH) / 'config' / 'json_files'

    @classmethod
    def _validate_file_exists(cls, file_path):
        """
        验证文件是否存在
        :param file_path: 文件路径
        :return: Path 对象
        :raises: JsonFileNotFoundError
        """
        path = Path(file_path)
        if not path.exists():
            error_msg = f'JSON 文件不存在: {path}'
            logger.error(error_msg)
            raise JsonFileNotFoundError(error_msg)
        return path

    @classmethod
    def read_json(cls, json_file_name):
        """
        读取 JSON 文件
        
        :param json_file_name: JSON 文件名
        :return: 解析后的 JSON 数据
        :raises: JsonFileNotFoundError, Exception
        """
        file_path = cls.CONFIG_DIR / json_file_name

        try:
            # 验证文件存在
            cls._validate_file_exists(file_path)

            # 读取 JSON 文件
            with open(file_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
                logger.debug(f'成功读取 JSON 文件: {file_path}')
                return json_data

        except JsonFileNotFoundError:
            raise
        except json.JSONDecodeError as e:
            error_msg = f'JSON 解析错误 ({file_path}): {str(e)}'
            logger.error(error_msg)
            raise
        except Exception as e:
            error_msg = f'读取 JSON 文件出错 ({file_path}): {str(e)}'
            logger.error(error_msg)
            raise

    @classmethod
    def validate_json_schema(cls, json_data, json_schema, log_name='schema.log'):
        """
        校验 JSON 数据是否符合指定的 Schema
        
        :param json_data: 要校验的 JSON 数据
        :param json_schema: JSON Schema 定义
        :param log_name: 日志文件名
        :return: True 表示校验通过，False 表示校验失败
        """
        schema_logger = get_log(log_name)

        try:
            # 执行 Schema 校验
            jsonschema.validate(json_data, schema=json_schema)
            logger.debug('JSON Schema 校验通过')
            return True

        except jsonschema.SchemaError as e:
            # Schema 定义本身有问题
            error_location = ' --> '.join(str(i) for i in e.path) if e.path else '根节点'
            error_msg = f'Schema 定义错误\n位置: {error_location}\n信息: {e.message}'
            schema_logger.error(error_msg)
            logger.error(f'Schema 校验失败: {error_msg}')
            return False

        except jsonschema.ValidationError as e:
            # JSON 数据不符合 Schema 定义
            error_path = ' --> '.join(str(i) for i in e.path) if e.path else '根节点'
            error_msg = f'JSON 数据不符合 Schema 规定\n字段: {error_path}\n信息: {e.message}'
            schema_logger.error(error_msg)
            logger.error(f'数据校验失败: {error_msg}')
            return False

        except Exception as e:
            error_msg = f'JSON Schema 校验异常: {str(e)}'
            schema_logger.error(error_msg)
            logger.error(error_msg)
            return False

    @classmethod
    def schemaJsonData(cls, json_data, json_schema):
        """
        校验 JSON 数据（向后兼容接口）
        
        :param json_data: 要校验的 JSON 数据
        :param json_schema: JSON Schema 定义
        :return: True 表示校验通过，False 表示校验失败
        """
        return cls.validate_json_schema(json_data, json_schema)


# 保持向后兼容性
class Json(JsonHelper):
    """向后兼容的 Json 类"""

    @staticmethod
    def read_json(json_file_name):
        """读取 JSON 文件（兼容旧接口）"""
        return JsonHelper.read_json(json_file_name)

    @staticmethod
    def schemaJsonData(json_data, json_schema):
        """校验 JSON Schema（兼容旧接口）"""
        return JsonHelper.validate_json_schema(json_data, json_schema)

