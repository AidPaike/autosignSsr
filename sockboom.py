import requests
import json
import os
import time
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}
email = 'f335125303@163.com'
passwd = 'Ff1314521...'
loginData = {"email": email, "passwd": passwd}  # 需要填写sockboom登录信息
contents = ''


def output(content):
    global contents
    contents += '\n' + content
    print(content)


def sign(header):
    url = 'https://sockboom.app/auth/login'
    print(url)
    response = requests.post(url=url, data=loginData)
    print(response.content)

    sign_message = json.loads(response.content)['msg']
    user = json.loads(response.content)['user']
    output('  [+]' + sign_message + '，用户：' + user)
    cookie = response.headers
    cookie_uid = cookie['Set-Cookie'].split('/')[0].split(';')[0]
    cookie_email = 'f335125303@163.com'
    cookie_key = cookie['Set-Cookie'].split('/')[2].split(';')[0].split(',')[1]
    cookie_ip = cookie['Set-Cookie'].split('/')[3].split(';')[0].split(',')[1]
    cookie_expire_in = cookie['Set-Cookie'].split('/')[4].split(';')[
        0].split(',')[1]
    Cookie = cookie_uid + ';' + cookie_email + ';' + \
             cookie_key + ';' + cookie_ip + ';' + cookie_expire_in
    print(Cookie)
    return Cookie


def user_centre(cookie):  # 用户中心
    url = 'https://sockboom.app/user'
    headers = {
        'Cookie': cookie
    }
    response = requests.get(url=url, headers=headers, verify=False)
    soup = BeautifulSoup(response.content, 'html.parser')  # 解析html页面
    # 获取个人用户信息
    pims = soup.select('.dash-card-content h3')
    pim = [pim for pim in pims]
    # print(pims)
    output('  [+]用户等级:' + pim[0].string)
    output('  [+]账户余额:' + pim[1].text.split('\n')[0])
    output('  [+]在线设备:' + pim[2].text.split('\n')[0])
    output('  [+]宽带速度:' + pim[3].string)
    # 获取流量信息
    flows = soup.select('span[class="pull-right strong"]')
    flow = [flow.string for flow in flows]
    output('  [+]总流量:' + flow[0])
    output('  [+]使用流量:' + flow[1])
    output('  [+]剩余流量:' + flow[2])
    output('  [+]可用天数:' + flow[3])
    return headers


def checkin(headers):
    url = 'https://sockboom.app/user/checkin'
    response = requests.post(url=url, headers=headers, verify=False)
    msg = json.loads(response.content)['msg']
    output('  [+]签到信息:' + msg)
    now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with open("run.log", "a") as f:
        f.write(f"sockboom---->{now_time},{msg}\n")


def main():
    cookie = sign(header)
    headers = user_centre(cookie)
    checkin(headers)


def main_handler(event, context):
    return main()


if __name__ == '__main__':
    main()
