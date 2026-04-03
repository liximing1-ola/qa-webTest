import requests


def robot(mode, reason, bot='rank', title='', color="good"):
    headers = {'Content-Type': 'application/json'}
    #  企微
    robot_dict_wechat = {
        'rank': 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=0179d8d1-2078-41ba-a8da-0fb11bd51880',
        'BB': 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=f9d916cb-6b93-4389-8aa4-f51c755faa0e'}
    url = robot_dict_wechat[bot]
    if mode == 'fail':
        content = f"警告！失败用例：{title}, 失败原因：{reason}"
        data = {
            "msgtype": "text",
            "text": {
                "content": content
            }
        }
        r = requests.post(url, headers=headers, json=data)
        if r.status_code == 200 and r.text.find('ok'):
            data = {
                "msgtype": "text",
                "text": {
                    "mentioned_mobile_list": ["all"]
                }
            }
            requests.post(url, headers=headers, json=data)

    elif mode == 'success':
        data = {
            "msgtype": "text",
            "text": {
                "content": reason
            }
        }
        requests.post(url, headers=headers, json=data)

    elif mode == 'markdown':
        data = {
            "msgtype": "markdown",
            "markdown": {
                "content": reason
            }
        }
        requests.post(url, headers=headers, json=data)

    elif mode == 'slack':
        data = {
            "attachments": [
                {
                    "fallback": "",
                    "pretext": "",
                    "color": color,
                    "fields": [
                        {
                            "title": title,
                            "value": reason,
                            "short": 0
                        }
                    ]
                }
            ]
        }
        requests.post(url, headers=headers, json=data)

    elif mode == 'slack_pt':
        data = {
            "title": title,
            "value": reason,
        }
        requests.post(url, headers=headers, json=data)

    else:
        print('robot over gg')
