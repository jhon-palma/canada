import smtplib
from email.mime.text import MIMEText


def sendEmail(content):
    servidor_smtp = 'smtp.gmail.com'
    puerto_smtp = 587
    user = 'icloudcris@gmail.com'
    password = 'umqh nftk hhau eofp'

    msg = MIMEText(content)
    msg['Subject'] = 'Reporte LJ Realties'
    msg['From'] = user
    msg['To'] = 'jhon1946@gmail.com'

    try:
        with smtplib.SMTP(servidor_smtp, puerto_smtp) as server:
            server.starttls()
            server.login(user, password)
            server.sendmail(user, [msg['To']], msg.as_string())
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
