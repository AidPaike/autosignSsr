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
passwd = 'fanzhenye@666'
loginData = {"email": email, "passwd": passwd}  # 需要填写sockboom登录信息
contents = ''

def output(content):
    global contents
    contents += '\n' + content
    print(content)


def sign(header):
    url = 'https://ssrla.de/auth/login'
    response = requests.post(url=url, data=loginData)
    # print(response.content)
    # print(response.text)
    sign_message = json.loads(response.content)
    # print(sign_message)
    cookie = response.headers
    cookie_uid = cookie['Set-Cookie'].split('/')[0].split(';')[0]
    cookie_email = 'f335125303@163.com'
    cookie_key = cookie['Set-Cookie'].split('/')[2].split(';')[0].split(',')[1]
    cookie_ip = cookie['Set-Cookie'].split('/')[3].split(';')[0].split(',')[1]
    cookie_expire_in = cookie['Set-Cookie'].split('/')[4].split(';')[
        0].split(',')[1]
    Cookie = '''crisp-client%2Fsession%2F1ae3ebbe-7b15-4192-93fd-0a86bc7f22df=session_18165a6b-e009-43dd-b300-a15fcd6c7b10;crisp-client%2Fsession%2F1ae3ebbe-7b15-4192-93fd-0a86bc7f22df%2F8f9b0e06-0e3b-3a6e-bfc9-a82342206d3a=session_18165a6b-e009-43dd-b300-a15fcd6c7b10;'''\
             + cookie_uid + ';' + 'email='+cookie_email + ';' + \
             cookie_key + ';' + cookie_ip + ';' + cookie_expire_in
    return Cookie

def user_centre(cookie):  # 用户中心
    url = 'https://ssrla.de/user'
    headers = {
        'Cookie': "crisp-client%2Fsession%2F1ae3ebbe-7b15-4192-93fd-0a86bc7f22df=session_18165a6b-e009-43dd-b300-a15fcd6c7b10; crisp-client%2Fsession%2F1ae3ebbe-7b15-4192-93fd-0a86bc7f22df%2F8f9b0e06-0e3b-3a6e-bfc9-a82342206d3a=session_18165a6b-e009-43dd-b300-a15fcd6c7b10; uid=6496; email=f335125303%40163.com; key=52e442647e3b6efff04d53bfe41aea544d941d6ae3836; ip=0069911ae1d99e8325bca46798fcd7d4; expire_in=1660956560"
    }
    response = requests.get(url=url, headers=headers, verify=False)
    soup = BeautifulSoup(response.content, 'html.parser')  # 解析html页面
    # print(response.text)
    # 获取个人用户信息
    pims = soup.select('.product-result')
    pim = [pim.text for pim in pims]
    output('  [+]剩余流量:' + pim[0].split('\n')[1])
    output('  [+]今日已用:' + pim[1].split('\n')[1])
    output('  [+]历史使用:' + pim[2].split('\n')[1])
    return headers,pim

def checkin(headers,pim):
    url = 'https://ssrla.de/user/checkin'
    response = requests.post(url=url, headers=headers, verify=False)
    msg = json.loads(response.content)['msg']
    output('  [+]签到信息:' + msg)
    now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    p1 = pim[0].split('\n')[1]
    p2 = pim[1].split('\n')[1]
    p3 = pim[2].split('\n')[1]
    with open("run.log", "a") as f:
        f.write(f"ssr---->{now_time},{msg},剩余流量:{p1},今日已用:{p2},历史使用:{p3}\n")


if __name__ == '__main__':
    cookie = sign(header)
    headers,pim = user_centre(cookie)
    checkin(headers,pim)