# 此接口支持发送验证码短信、订单通知短信；
# 调试期间，请使用测试专用短信模板：您的验证码是：1234。请不要把验证码泄露给其他人。
# 请求参数中的account和password分别为 APIID、APIKEY，请在本页面上方处获取。

# python3

import urllib.parse
import urllib.request

from apscheduler.schedulers.blocking import BlockingScheduler
import time
import datetime

def message_send(phone_num, day_num):
    # 接口地址
    url = 'http://106.ihuyi.com/webservice/sms.php?method=Submit'

    # 定义请求的数据
    values = {
        'account': 'xxxxxxx',
        'password': 'xxxxxxxxxxxxxxxxxx',
        'mobile': phone_num,
        'content': f'您好，今天是核酸抽检第{day_num}天，不要忘记「18:00-21:00」前往「工会俱乐部」进行核酸检测，谢谢！',
        'format': 'json',
    }

    # 将数据进行编码
    data = urllib.parse.urlencode(values).encode(encoding='UTF8')

    # 发起请求
    req = urllib.request.Request(url, data)
    response = urllib.request.urlopen(req)
    res = response.read()

    # 打印结果
    print(res.decode("utf8"))

if __name__ == '__main__':
    phone_nums_list = []
    with open('./phone.list', 'r') as f:
        while True:
            line = f.readline().strip()
            if line:
                phone_num, day, day_interval, day_num = line.split()
                phone_nums_list.append([phone_num, day, int(day_interval), day_num])
            else:
                break
    print(phone_nums_list)

    print(datetime.datetime.now())

    # 实例化一个调度器
    scheduler = BlockingScheduler()

    def myjob(para):
        print(f'{para}, hello world!')

    for phone_info in phone_nums_list:
        scheduler.add_job(message_send, 'interval', days=phone_info[2], start_date=f'{phone_info[1]} 17:00:00', args=[phone_info[0], phone_info[3]])

    scheduler.start()



