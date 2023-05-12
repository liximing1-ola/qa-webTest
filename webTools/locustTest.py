# coding=utf-8
from locust import HttpUser, TaskSet, task, between
import urllib3
import urllib.parse
urllib3.disable_warnings()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # 禁用安全请求警告


# Number of users to simulate：设置模拟的用户总数
# Hatch rate (users spawned/second)：每秒启动的虚拟用户数
class InterfaceConcurrency(TaskSet):

    @task(0)
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

    @task(0)
    def on_banban_consume_single(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko)\
                              Chrome/67.0.3396.99 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
            "user-token": "0171XGrjmkju7__2FnbI0LsBgPzjXAuei__2FPGt0eb4mYwEB7sms72l7rX0Uft1__2Fiwam0lN5TlgN__2FyrgYlSH__2FYBpJMtVD__2BYFNeQucvtMjy6hGszs__2BZ4EIVN7Ks8I8"
        }
        url = "https://192.168.11.46/pay/create?package=com.imbb.banban.android"
        payload = 'platform=available&type=banban-consume&money=9600&params={"consume_type":"gift_combine","rid":200093221,"combine_id":1,"combine_type":1,"pay_receptor":{"gift_id":1406,"gift_num":1,"uid":"100287189"},"pay_gs":{"gift_id":1407,"gift_num":1,"uid":"100287189"},"useCoin":-1}'
        res = self.client.post(url, data=payload, headers=headers, verify=False)
        if res.status_code == 200:
            print(res.json())
        else:
            print(res.json())

    @task(0)
    def on_banban_consume_all(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko)\
                              Chrome/67.0.3396.99 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
            "user-token": "b688zBCcMO8ln__2B9__2BwrV0UBbK19HnXfliByIvv05liBpK4Rs26HvHaxeaL0oz8oK8SWgB__2F9PftRuXf__2F5Tu22mMaH7JmD5XzPXD9ZhEb__2FLsHJhS4u1xNOTsxmB"
        }
        url = "https://192.168.11.46/pay/create?package=com.imbb.banban.android"
        payload = 'platform=available&type=banban-consume&money=20400&params={"consume_type":"gift_combine","rid":200093221,"combine_id":2,"combine_type":2,"pay_creator":{"gift_id":628,"gift_num":2,"uid":"131542080"},"pay_receptor":{"gift_id":628,"gift_num":2,"uid":"100287189"},"pay_gs":{"gift_id":686,"gift_num":1,"uid":"100287189,100010055,131565153,100010057,100010058,100010060"},"useCoin":-1}'
        res = self.client.post(url, data=payload, headers=headers, verify=False)
        if res.status_code == 200:
            print(res.json())
        else:
            print(res.json())

    @task(100)
    def panelGift(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko)\
                              Chrome/67.0.3396.99 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
            "user-token": "20f15zXeW0ntECmA21qc3oNJG35__2FU8BT2R5tLnkw__2F2vBh8SJN9o__2F9eUOKcFbZyx8l0__2FMKdNUMO4IJEdoHJFCPa9Jz__2FcTIQhvOFuppFkEzTFJDywP5qXYiB0G"
        }
        url = "https://192.168.11.46/pay/create?package=com.imbb.banban.android"
        payload = 'platform=available&type=package&money=999900&params={"room_ticket":1,"price":999900,"rid":200093620,"uids":"100287189","giftId":21,"giftNum":1,"version":2,"gift_type":"normal","useCoin":-1}'
        res = self.client.post(url, data=payload, headers=headers, verify=False)
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
