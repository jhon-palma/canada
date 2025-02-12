import smtplib
from email.mime.text import MIMEText
from immobilier.settings import DEBUG


def sendEmail(sender, destinatary, subject, content):

    if DEBUG or sender == 'icloudcris@gmail.com':
        user = 'icloudcris@gmail.com'
        password = 'umqh nftk hhau eofp'
        destinatary = 'backups@remaxplatinum.pe'
    else:
        user = 'mar@ljrealties.com'
        password = 'ndrj mpwg mxfn cnrb'

    message = MIMEText(content)
    message.set_charset('utf-8')
    message['Subject'] = str(subject)
    message['From'] = user
    message['To'] = destinatary

    try: 
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(user, password)
        server.sendmail(user, destinatary, message.as_string())
        server.quit()
    except: pass
        


