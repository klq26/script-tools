import smtplib
from email.mime.text import MIMEText
from email.header import Header

class emailMessager:

    def __init__(self):
        self.from_address = 'klq26@qq.com'
        # https://service.mail.qq.com/cgi-bin/help?subtype=1&&id=28&&no=1001256%27)
        # 授权码许登录 mail.qq.com 进入“设置”、“账户”，找到 POP3 部分，打开 POP3/STMP 服务，然后点击“生成授权码”
        # 每次变更邮箱密码，都需要通过手机号重新生成。
        self.authorizatioCode = 'gejelhbulxaxbiaa'
        self.to_addr = 'klq26@163.com'

    def send(self, to_address = 'klq26@163.com', subject = '测试标题', msg = '测试正文'):
        # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
        msg = MIMEText(msg,'plain','utf-8')
        # 邮件信息
        msg['From'] = Header(self.from_address)
        msg['To'] = Header(to_address)
        msg['Subject'] = Header(subject)
        try:
            client = smtplib.SMTP_SSL('smtp.qq.com', smtplib.SMTP_SSL_PORT)
            client.login(self.from_address, self.authorizatioCode)
            client.sendmail(self.from_address, to_address, msg.as_string())
        except smtplib.SMTPException as e:
            print("[ERROR] 发送邮件异常：{0}".format(e))
        finally:
            client.quit()

if __name__ == "__main__":
    emailMessager().send()

