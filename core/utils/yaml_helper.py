"""
YAML 配置文件处理模块
"""
import yaml
import os
from pathlib import Path
from core.utils.logger import get_log
from core.config.settings import config

logger = get_log('yaml.log')


class YamlFileNotFoundError(Exception):
    """YAML 文件不存在异常"""
    pass


class YamlDataNotFoundError(Exception):
    """YAML 数据不存在异常"""
    pass


class YamlHelper:
    """YAML 文件读取辅助类"""

    # 配置文件目录
    CONFIG_DIR = Path(config.BASE_PATH) / 'config' / 'yaml_files'

    @classmethod
    def _validate_file_exists(cls, file_path):
        """
        验证文件是否存在
        :param file_path: 文件路径
        :return: Path 对象
        :raises: YamlFileNotFoundError
        """
        path = Path(file_path)
        if not path.exists():
            error_msg = f'YAML 文件不存在: {path}'
            logger.error(error_msg)
            raise YamlFileNotFoundError(error_msg)
        return path

    @classmethod
    def _load_yaml_file(cls, file_path):
        """
        加载 YAML 文件
        :param file_path: 文件路径
        :return: 解析后的 YAML 数据
        :raises: Exception
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.load(f, Loader=yaml.SafeLoader)
                if data is None:
                    raise YamlDataNotFoundError(f'YAML 文件为空: {file_path}')
                logger.debug(f'成功加载 YAML 文件: {file_path}')
                return data
        except yaml.YAMLError as e:
            error_msg = f'YAML 解析错误 ({file_path}): {str(e)}'
            logger.error(error_msg)
            raise
        except Exception as e:
            error_msg = f'读取 YAML 文件出错 ({file_path}): {str(e)}'
            logger.error(error_msg)
            raise

    @classmethod
    def read_yaml(cls, yaml_file_name, yaml_key=None):
        """
        读取 YAML 文件中的数据
        
        :param yaml_file_name: YAML 文件名
        :param yaml_key: 要读取的键（可选，不指定则返回整个文件）
        :return: YAML 数据
        :raises: YamlFileNotFoundError, YamlDataNotFoundError
        """
        # 构建完整路径
        file_path = cls.CONFIG_DIR / yaml_file_name

        try:
            # 验证文件存在
            cls._validate_file_exists(file_path)

            # 加载 YAML 文件
            yaml_data = cls._load_yaml_file(file_path)

            # 如果指定了键，则返回该键的值
            if yaml_key:
                if yaml_key not in yaml_data:
                    error_msg = f'YAML 键不存在: {yaml_key} (文件: {yaml_file_name})'
                    logger.error(error_msg)
                    raise YamlDataNotFoundError(error_msg)

                value = yaml_data[yaml_key]
                if value is None:
                    error_msg = f'YAML 键值为空: {yaml_key} (文件: {yaml_file_name})'
                    logger.warning(error_msg)

                return value

            return yaml_data

        except (YamlFileNotFoundError, YamlDataNotFoundError):
            raise
        except Exception as e:
            logger.error(f'读取 YAML 文件失败: {str(e)}')
            raise


# 保持向后兼容性
class Yaml(YamlHelper):
    """向后兼容的 Yaml 类"""

    @staticmethod
    def read_yaml(yaml_file_name, yaml_name):
        """
        读取 YAML 文件（兼容旧接口）
        
        :param yaml_file_name: YAML 文件名
        :param yaml_name: YAML 键名
        :return: YAML 数据
        """
        return YamlHelper.read_yaml(yaml_file_name, yaml_name)
