import json
import requests
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

loginUrl = "https://sockboom.lol/auth/login"
checkinUrl = "https://sockboom.lol/user/checkin"
lououtUrl = "https://sockboom.lol/user/logout"
loginData = {"email": "f335125303@163.com", "passwd": "Ff1314521..."}  # 需要填写sockboom登录信息
my_sender = ''  # 邮件发送者
my_pass = ''  # 授权码
my_user = ''  # 邮件接收者(可以和发送者相同)


def checkin():
    r = requests.session()
    try:
        loginRes = r.post(loginUrl, data=loginData)
        print(loginRes.content)
        loginResJson = json.loads(loginRes.content)
        if loginResJson['ret'] == 1:
            print("success login")
    except:
        print("fail login")
        return False

    try:
        checkinRes = r.post(checkinUrl)
        checkinResJson = json.loads(checkinRes.text)
        assert checkinResJson['ret'] == 1
        print("success checkin")
        print(checkinResJson['msg'])
    except:
        print("fail checkin")
        return False

    logout = r.get(lououtUrl)
    return checkinResJson['msg']


def mail(msg):
    try:
        msg = MIMEText(msg, 'plain', 'utf-8')
        msg['From'] = formataddr(["FromRunoob", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["FK", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "Sockboom签到状态提醒"  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()
        return True
    except Exception:
        print("邮件发送失败")
        return False


if __name__ == "__main__":

    checkinRes = checkin()
    # if checkinRes:
    #     ret = mail(checkinRes)
    #     if ret:
    #         print("签到成功,邮件发送成功")
    #     else:
    #         print("签到成功，邮件发送失败")
    # else:
    #     ret = mail("签到失败")
    #     if ret:
    #         print("签到失败,邮件发送成功")
    #     else:
    #         print("签到失败，邮件发送失败")
