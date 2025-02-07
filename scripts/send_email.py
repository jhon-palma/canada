import smtplib
from email.mime.text import MIMEText
from immobilier.settings import DEBUG


def sendEmail(sender, destinatary, subject, content):
    servidor_smtp = 'smtp.gmail.com'
    puerto_smtp = 587

    if DEBUG or sender == 'icloudcris@gmail.com':
        user = 'icloudcris@gmail.com'
        password = 'umqh nftk hhau eofp'
        destinatary = 'backups@remaxplatinum.pe'
    else:
        user = 'mar@ljrealties.com'
        password = 'ndrj mpwg mxfn cnrb'

    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = user
    msg['To'] = destinatary

    try:
        with smtplib.SMTP(servidor_smtp, puerto_smtp) as server:
            server.starttls()
            server.login(user, password)
            server.sendmail(user, [msg['To']], msg.as_string())
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
