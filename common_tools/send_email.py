from email.mime.text import MIMEText
from email.header import Header
import smtplib
from common_tools import conf
from common_tools import sql_monitor_style


def send_email_by_csr(content, subject, receiver):
    """
    其余配置如发件人从配置文件读取
    :param content: 邮件正文
    :param subject: 邮件标题
    :param receiver: 接收人  多人以逗号分隔
    :return:
    """
    email_args = conf.get_email_args()
    password = email_args['password']
    sender = email_args['addr']
    msg = MIMEText(content, 'html', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = "%s <%s>" % (email_args['from'], sender)
    msg['to'] = receiver
    stmp = smtplib.SMTP()
    stmp.connect(email_args['server'])
    stmp.login(sender, password)
    stmp.sendmail(sender, receiver.split(","), msg.as_string())
    stmp.quit()


def send_email_with_style(result, count, title, content_append=''):
    """content_append 可为空 """
    receiver = conf.get_email_args()['to']
    style = sql_monitor_style.style
    content = "<style>" + style + "</style>"
    content += result.to_html(header=True, border=0, classes='table15_1', index=False)
    content += '\n\n<br/><br/>结果共<font style="color:red">{}</font>条<br/><br/>\n\n'.format(count)
    if len(content_append) > 0:
        content += '部分用户在平台无冻结订单，可直接解冻。命令参考如下：\n<br/>'
        content += content_append
    send_email_by_csr(content, title, receiver)


if __name__ == '__main__':
    content_test = '测试正文'
    subject_test = '测试主题'
    send_email_by_csr(content_test, subject_test, 'test@test.com')
