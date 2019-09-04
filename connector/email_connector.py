import smtplib
from email.mime.text import MIMEText
from email.header import Header


def emailSend(mailGroup,subject,content):
    try:
        message = MIMEText("<h1>'%s'</h1><p>Xiaochen Tan</p>"%content,'html')
        message['From'] = mailGroup['sender']
        message['To'] = mailGroup['receivers'][0]
        message['Subject'] = Header(subject, 'utf-8')

        smtp = smtplib.SMTP_SSL(mailGroup['mailHost'], mailGroup['port'])
        smtp.login(mailGroup['userName'], mailGroup['password'])
        smtp.sendmail(mailGroup['sender'], mailGroup['receivers'], message.as_string())
        smtp.close
        return 'Email send successfully!'

    except smtplib.SMTPException:
        return 'Email send failed...'

def alarmGroupAdmin():
    return {
        'mailHost': 'smtp.163.com',
        'port': 465,
        'userName': 'pythonalarm@163.com',
        'password': 'pythonalarmcode',
        'sender': "pythonalarm@163.com",
        'receivers': ["13911326361@139.com"]
    }
