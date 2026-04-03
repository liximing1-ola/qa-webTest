import yaml
from core.utils.logger import get_log
from core.config.settings import config
import os


class Yaml:

    @staticmethod
    def read_yaml(yaml_fileName, yaml_name):
        """
        读取 yaml
        :return: yaml_data
        """
        yaml_path = config.BASE_PATH + '/config/yaml_files/' + yaml_fileName
        try:
            if not os.path.exists(yaml_path):
                get_log('read_yaml.log').error(f'文件地址-{yaml_path} 不存在')
                return FileExistsError
            yaml_data = yaml.load(open(yaml_path, 'r', encoding='utf-8'), Loader=yaml.SafeLoader)  # 添加后不会报 warning
            if yaml_data[yaml_name] is None:
                return TypeError
            else:
                return yaml_data[yaml_name]
        except Exception as e:
            get_log('read_yaml.log').error(f'读取{yaml_path} 文件报错，错误是{e}')
