import json
from common import Logs
import os
from common.Config import config
import jsonschema


#  参考路径：https://www.cnblogs.com/ChangAn223/p/11234348.html
class Json:

    @staticmethod
    def read_json(json_fileName):
        """
        读取json文件
        :return:
        """
        json_path = config.BASE_PATH + '/conf/json_File/' + json_fileName
        try:
            if not os.path.exists(json_path):
                Logs.get_log('read_json.log').error('文件地址: {} 不存在'.format(json_path))
                return FileExistsError
            with open(json_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
                return json_data
        except Exception as e:
            Logs.get_log('read_json.log').error('读取{} 文件报错，错误是:{}'.format(json_path, e))

    @staticmethod
    def schemaJsonData(json_data, json_schema):
        """
        校验Schema json数据
        :return:
        """
        try:
            jsonschema.validate(json_data, schema=json_schema)
            return True
        except jsonschema.SchemaError as e1:
            Logs.get_log('schema.log').error("验证模式schema出错：\n出错位置: {} \n提示信息: {}"
                                             .format(" --> ".join([i for i in e1.path]), e1.message, json_data))
            return False
        except jsonschema.ValidationError as e2:
            Logs.get_log('schema.log').error("json数据不符合schema规定：\n出错字段：{} \n提示信息：{}"
                                             .format(" --> ".join(['%s' % i for i in e2.path]), e2.message, json_data))
            return False
        except Exception as e:
            Logs.get_log('schema.log').error(e)
            return False