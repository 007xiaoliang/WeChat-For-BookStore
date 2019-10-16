import smtplib
from email.mime.text import MIMEText


def sentemail(order_code):
    host = 'smtp.163.com'
    # 设置发件服务器地址
    port = 465
    # 设置发件服务器端口号。注意，这里有SSL和非SSL两种形式，现在一般是SSL方式
    sender = '15211120934@163.com'
    # 设置发件邮箱，一定要自己注册的邮箱
    pwd = 'SGJEKFBFK322'
    # 设置发件邮箱的授权码密码，根据163邮箱提示，登录第三方邮件客户端需要授权码
    receiver = '1352807232@qq.com'
    # 设置邮件接收人，可以是QQ邮箱
    body = '<h1>系统有新的订单,订单号为:' + order_code + '</h1><br><p>系统消息，请勿回复</p>'
    # 设置邮件正文，这里是支持HTML的
    msg = MIMEText(body, 'html')
    # 设置正文为符合邮件格式的HTML内容
    msg['subject'] = '新订单通知'
    # 设置邮件标题
    msg['from'] = sender
    # 设置发送人
    msg['to'] = receiver
    # 设置接收人
    try:
        s = smtplib.SMTP_SSL(host, port)
        # 注意！如果是使用SSL端口，这里就要改为SMTP_SSL
        s.login(sender, pwd)
        # 登陆邮箱
        s.sendmail(sender, receiver, msg.as_string())
    except smtplib.SMTPException:
        print('Error.sent email fail')


if __name__ == '__main__':
    sentemail()
