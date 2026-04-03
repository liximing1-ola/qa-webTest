# coding=utf-8
from locust import HttpUser, TaskSet, task, between
import urllib3
import urllib.parse
import json

urllib3.disable_warnings()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # 禁用安全请求警告


# ==================== 配置管理 ====================
BASE_URL = "https://192.168.11.46"
PACKAGE = "com.imbb.banban.android"
DEFAULT_HEADERS_BASE = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded",
}

# 测试用例配置
TEST_CASES = {
    "on_init": {
        "url": f"{BASE_URL}/pay/create",
        "user_token": "0976FcAmUaHnJvJAKi804Ijs2Cm3__2BuamYTrhAVV9baYv2cOWvvuwII2kdNeSKeB8MGHOnQJq878fOl3VKNltq4__2BP7pfIksSLlQs1Y4s50wqo__2Fm3qksqrXTqC",
        "weight": 0,
    },
    "on_banban_consume_single": {
        "url": f"{BASE_URL}/pay/create",
        "user_token": "0171XGrjmkju7__2FnbI0LsBgPzjXAuei__2FPGt0eb4mYwEB7sms72l7rX0Uft1__2Fiwam0lN5TlgN__2FyrgYlSH__2FYBpJMtVD__2BYFNeQucvtMjy6hGszs__2BZ4EIVN7Ks8I8",
        "weight": 0,
    },
    "on_banban_consume_all": {
        "url": f"{BASE_URL}/pay/create",
        "user_token": "b688zBCcMO8ln__2B9__2BwrV0UBbK19HnXfliByIvv05liBpK4Rs26HvHaxeaL0oz8oK8SWgB__2F9PftRuXf__2F5Tu22mMaH7JmD5XzPXD9ZhEb__2FLsHJhS4u1xNOTsxmB",
        "weight": 0,
    },
    "panelGift": {
        "url": f"{BASE_URL}/pay/create",
        "user_token": "20f15zXeW0ntECmA21qc3oNJG35__2FU8BT2R5tLnkw__2F2vBh8SJN9o__2F9eUOKcFbZyx8l0__2FMKdNUMO4IJEdoHJFCPa9Jz__2FcTIQhvOFuppFkEzTFJDywP5qXYiB0G",
        "weight": 100,
    },
}

# 请求数据配置
PAYLOADS = {
    "on_init": {
        "is_json": True,
        "data": {
            "platform": "available",
            "type": "package",
            "money": 200,
            "params": {
                "rid": 200057467,
                "uids": "105000355",
                "positions": "1",
                "position": -1,
                "giftId": 2602,
                "giftNum": 1,
                "price": 200,
                "cid": 0,
                "ctype": "",
                "duction_money": 0,
                "version": 2,
                "num": 1,
                "gift_type": "normal",
                "useCoin": -1,
                "star": 0,
                "show_pac_man_guide": 1,
                "refer": "",
                "all_mic": 0,
                "egg_level": "1",
            },
        },
    },
    "on_banban_consume_single": {
        "is_json": False,
        "data": 'platform=available&type=banban-consume&money=9600&params={"consume_type":"gift_combine","rid":200093221,"combine_id":1,"combine_type":1,"pay_receptor":{"gift_id":1406,"gift_num":1,"uid":"105000355"},"pay_gs":{"gift_id":1407,"gift_num":1,"uid":"105000355"},"useCoin":-1}',
    },
    "on_banban_consume_all": {
        "is_json": False,
        "data": 'platform=available&type=banban-consume&money=20400&params={"consume_type":"gift_combine","rid":200093221,"combine_id":2,"combine_type":2,"pay_creator":{"gift_id":628,"gift_num":2,"uid":"131542080"},"pay_receptor":{"gift_id":628,"gift_num":2,"uid":"105000355"},"pay_gs":{"gift_id":686,"gift_num":1,"uid":"105000355,100010055,131565153,100010057,100010058,100010060"},"useCoin":-1}',
    },
    "panelGift": {
        "is_json": False,
        "data": 'platform=available&type=package&money=999900&params={"room_ticket":1,"price":999900,"rid":200093620,"uids":"105000355","giftId":21,"giftNum":1,"version":2,"gift_type":"normal","useCoin":-1}',
    },
}


class InterfaceConcurrency(TaskSet):
    """接口并发测试任务集 - 模拟用户并发行为"""

    def _prepare_request(self, case_name):
        """
        准备请求参数 - 统一处理所有请求的准备工作
        :param case_name: 用例名称
        :return: url, data, headers
        """
        case_config = TEST_CASES[case_name]
        payload_config = PAYLOADS[case_name]

        # 构建请求头
        headers = DEFAULT_HEADERS_BASE.copy()
        headers["user-token"] = case_config["user_token"]

        # 构建请求 URL
        url = f"{case_config['url']}?package={PACKAGE}"

        # 处理请求体
        if payload_config["is_json"]:
            # 需要编码的 JSON 数据
            data = urllib.parse.urlencode(payload_config["data"])
            data = data.replace("+", "").replace("%27", "%22")
        else:
            # 直接使用预定义的数据
            data = payload_config["data"]

        return url, data, headers

    def _handle_response(self, response, case_name):
        """
        处理响应 - 统一的响应处理逻辑
        :param response: 响应对象
        :param case_name: 用例名称
        """
        try:
            result = response.json()
            status = "✓" if response.status_code == 200 else "✗"
            print(f"[{status}] {case_name}: {response.status_code}")
            if response.status_code != 200:
                print(f"    Error: {result}")
        except Exception as e:
            print(f"[✗] {case_name}: JSON 解析失败 - {str(e)}")

    @task(0)
    def on_init(self):
        """初始化任务 - 用户加钱"""
        url, data, headers = self._prepare_request("on_init")
        response = self.client.post(url, data=data, headers=headers, verify=False)
        self._handle_response(response, "on_init")

    @task(0)
    def on_banban_consume_single(self):
        """单笔消费任务"""
        url, data, headers = self._prepare_request("on_banban_consume_single")
        response = self.client.post(url, data=data, headers=headers, verify=False)
        self._handle_response(response, "on_banban_consume_single")

    @task(0)
    def on_banban_consume_all(self):
        """全部消费任务"""
        url, data, headers = self._prepare_request("on_banban_consume_all")
        response = self.client.post(url, data=data, headers=headers, verify=False)
        self._handle_response(response, "on_banban_consume_all")

    @task(100)
    def panelGift(self):
        """面板礼物任务 - 主要测试用例（权重最高）"""
        url, data, headers = self._prepare_request("panelGift")
        response = self.client.post(url, data=data, headers=headers, verify=False)
        self._handle_response(response, "panelGift")


class WebsiteUser(HttpUser):
    """网站用户压测模型"""

    tasks = [InterfaceConcurrency]
    wait_time = between(1, 3)  # 用户等待时间范围（秒）
    host = BASE_URL


if __name__ == "__main__":
    import os

    os.system(f"locust -f {__file__}")
