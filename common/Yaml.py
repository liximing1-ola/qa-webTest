import yaml
from common import Logs
from common.Config import config
import os


class Yaml:

    @staticmethod
    def read_yaml(yaml_fileName, yaml_name):
        """
        读取yaml
        :return: yaml_data
        """
        yaml_path = config.BASE_PATH + '/conf/yaml_File/' + yaml_fileName
        try:
            if not os.path.exists(yaml_path):
                Logs.get_log('read_yaml.log').error('文件地址-{} 不存在'.format(yaml_path))
                return FileExistsError
            yaml_data = yaml.load(open(yaml_path, 'r', encoding='utf-8'), Loader=yaml.FullLoader)  # 添加后不会报warning
            if yaml_data[yaml_name] is None:
                return TypeError
            else:
                return yaml_data[yaml_name]
        except Exception as e:
            Logs.get_log('read_yaml.log').error('读取{} 文件报错，错误是{}'.format(yaml_path, e))