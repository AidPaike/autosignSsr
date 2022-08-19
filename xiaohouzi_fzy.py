import requests
import json
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


def sign(header):
    url = 'https://www.xiaohouzilaaa.xyz/auth/login'
    print(url)
    response = requests.post(url=url, data=loginData)
    print(response.text)

    sign_message = json.loads(response.content)
    print(sign_message)
    cookie = response.headers
    cookie_uid = cookie['Set-Cookie'].split('/')[0].split(';')[0]
    cookie_email = 'f335125303@163.com'
    cookie_key = cookie['Set-Cookie'].split('/')[2].split(';')[0].split(',')[1]
    cookie_ip = cookie['Set-Cookie'].split('/')[3].split(';')[0].split(',')[1]
    cookie_expire_in = cookie['Set-Cookie'].split('/')[4].split(';')[
        0].split(',')[1]
    Cookie = "mtauth=c8be0c708ca4c9486a433bbd0ce255ef; pop=yes; lang=zh-cn;" + cookie_uid + ';' + 'email=' + cookie_email + ';' + \
             cookie_key + ';' + cookie_ip + ';' + cookie_expire_in + ";PHPSESSID=7eh43v0f5jcrbuej8jvgvbld67"
    return Cookie


def user_centre(cookie):  # 用户中心
    url = 'https://www.xiaohouzilaaa.xyz/user'
    headers = {
        'Cookie': "mtauth=c8be0c708ca4c9486a433bbd0ce255ef; pop=yes; lang=zh-cn; uid=64876; email=f335125303%40163.com; key=08512ae15326289e79e8660d7a60dfe6838d619b9c586; ip=0b80a9dc2efd883bb99f0ceb001accbe; expire_in=1661480824; PHPSESSID=7eh43v0f5jcrbuej8jvgvbld67"
    }
    response = requests.get(url=url, headers=headers, verify=False)
    soup = BeautifulSoup(response.content, 'html.parser')  # 解析html页面
    # print(response.text)
    # 获取个人用户信息
    pims = soup.select('.font-size-h4')
    pim = [pim.text for pim in pims]
    output('  [+]剩余会员时长:' + pim[0].split('\n')[1])
    output('  [+]剩余流量:' + pim[1].split('\n')[1])
    output('  [+]设备在线:' + pim[2].split('\n')[1])
    return headers, pim


def checkin(headers, pim):
    url = 'https://www.xiaohouzilaaa.xyz/user/checkin'
    response = requests.post(url=url, headers=headers, verify=False)
    msg = json.loads(response.content)['msg']
    output('  [+]签到信息:' + msg)
    now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    p1 = pim[0].split('\n')[1]
    p2 = pim[1].split('\n')[1]
    p3 = pim[2].split('\n')[1]
    with open("run.log", "a") as f:
        f.write(f"xiaohouzi---->{now_time},{msg},剩余会员时长:{p1},剩余流量:{p2},设备在线:{p3}\n")


if __name__ == '__main__':
    cookie = sign(header)
    # print(cookie)
    headers, pim = user_centre(cookie)
    checkin(headers, pim)
