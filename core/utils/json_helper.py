import json
from core.utils.logger import get_log
import os
from core.config.settings import config
import jsonschema


#  参考路径：https://www.cnblogs.com/ChangAn223/p/11234348.html
class Json:

    @staticmethod
    def read_json(json_fileName):
        """
        读取 json 文件
        :return:
        """
        json_path = config.BASE_PATH + '/config/json_files/' + json_fileName
        try:
            if not os.path.exists(json_path):
                get_log('read_json.log').error(f'文件地址：{json_path} 不存在')
                return FileExistsError
            with open(json_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
                return json_data
        except Exception as e:
            get_log('read_json.log').error(f'读取{json_path} 文件报错，错误是:{e}')

    @staticmethod
    def schemaJsonData(json_data, json_schema):
        """
        校验 Schema json 数据
        :return:
        """
        try:
            jsonschema.validate(json_data, schema=json_schema)
            return True
        except jsonschema.SchemaError as e1:
            get_log('schema.log').error("验证模式 schema 出错：\n出错位置：{} \n提示信息：{}".format(" --> ".join([i for i in e1.path]), e1.message, json_data))
            return False
        except jsonschema.ValidationError as e2:
            get_log('schema.log').error("json 数据不符合 schema 规定：\n出错字段：{} \n提示信息：{}".format(" --> ".join(['%s' % i for i in e2.path]), e2.message, json_data))
            return False
        except Exception as e:
            get_log('schema.log').error(e)
            return False
