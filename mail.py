#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header


def Sendmail(msg):
    mail_host = "smtp.126.com"
    mail_user = "itelephant@126.com"
    mail_pass = "xxxx"

    sender = 'itelephant@126.com'
    receivers = ['xxxx@dr-elephant.com','xxx@dr-elephant.com']

    message = MIMEText(msg, 'plain', 'utf-8')
    message['From'] = Header("itelephant@126.com")
    message['To'] = Header("itelephant@126.com")

    subject = '应用告警'
    message['Subject'] = Header(subject, 'utf-8')
    try:
        server = smtplib.SMTP_SSL(mail_host, 994)  # 第二个参数为默认端口为25，这里使用ssl，端口为994
        #print('开始登录')
        server.login(mail_user, mail_pass)  # 登录邮箱
        #print('登录成功')
        #print("邮件开始发送")
        server.sendmail(sender, receivers, message.as_string())
        server.quit()
        #print("邮件发送成功")
    except smtplib.SMTPException as e:
        print("邮件发送失败", e)


if __name__ == '__main__':
    Sendmail('test')