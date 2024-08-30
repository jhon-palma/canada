import smtplib
from email.mime.text import MIMEText


def sendEmail(sender, destinatary, subject, content):
    servidor_smtp = 'smtp.gmail.com'
    puerto_smtp = 587

    if sender == 'icloudcris@gmail.com':
        user = 'icloudcris@gmail.com'
        password = 'umqh nftk hhau eofp'
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
