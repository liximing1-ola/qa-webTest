# coding=utf-8
from locust import HttpUser, TaskSet, task, between
import urllib3
import urllib.parse
from common.Session import Session
urllib3.disable_warnings()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # 禁用安全请求警告


# Number of users to simulate：设置模拟的用户总数
# Hatch rate (users spawned/second)：每秒启动的虚拟用户数
class InterfaceConcurrency(TaskSet):

    @task
    def on_init(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko)\
                              Chrome/67.0.3396.99 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
            "user-token": "0976FcAmUaHnJvJAKi804Ijs2Cm3__2BuamYTrhAVV9baYv2cOWvvuwII2kdNeSKeB8MGHOnQJq878fOl3VKNltq4__2BP7pfIksSLlQs1Y4s50wqo__2Fm3qksqrXTqC"
            # "user-token": Session.get_session('dev')
        }
        url = "https://192.168.11.46/pay/create?package=com.imbb.banban.android"
        data = {
            "platform": "available",
            "type": "package",
            "money": 200,
            "params":
                {"rid": 200057467,
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
                 "gift_type": 'normal',
                 "useCoin": -1,
                 "star": 0,
                 "show_pac_man_guide": 1,
                 "refer": "",
                 "all_mic": 0,
                 "egg_level": "1"
                 }
        }
        d = urllib.parse.urlencode(data)
        data = d.replace('+', '').replace('%27', '%22')
        res = self.client.post(url, data=data, headers=headers, verify=False)
        if res.status_code == 200:
            print(res.json())
        else:
            print(res.json())


class websiteUser(HttpUser):
    tasks = [InterfaceConcurrency]
    wait_time = between(1, 3)  # s
    host = 'https://192.168.11.46/'  # http://localhost:8089/


if __name__ == "__main__":
    import os
    os.system("locust -f %s" % __file__)
