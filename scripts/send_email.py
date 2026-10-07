"""Envio de avisos por correo.

Las credenciales salen del .env. Antes estaban escritas aqui dentro -- dos
contrasenas de aplicacion de Gmail, en un archivo versionado --, y a cual de
las dos cuentas se enviaba lo decidia DEBUG, asi que el comportamiento del
correo dependia de un ajuste que no habla de correo.

Ahora son dos cosas dichas a proposito en el .env: con que cuenta se envia, y
si todo el correo se desvia a una direccion de pruebas en vez de ir a su
destinatario. En desarrollo se pone EMAIL_REDIRECT_TO; en produccion se deja
vacio.
"""

import smtplib
from email.mime.text import MIMEText

from django.conf import settings


def sendEmail(sender, destinatary, subject, content):
    usuario = settings.EMAIL_HOST_USER
    contrasena = settings.EMAIL_HOST_PASSWORD
    if not usuario or not contrasena:
        return

    if settings.EMAIL_REDIRECT_TO:
        destinatary = settings.EMAIL_REDIRECT_TO

    message = MIMEText(content)
    message.set_charset('utf-8')
    message['Subject'] = str(subject)
    message['From'] = usuario
    message['To'] = destinatary

    try:
        server = smtplib.SMTP('{}:{}'.format(settings.EMAIL_HOST, settings.EMAIL_PORT))
        server.starttls()
        server.login(usuario, contrasena)
        server.sendmail(usuario, destinatary, message.as_string())
        server.quit()
    except Exception:
        # Se traga el fallo a proposito, como antes: el envio es un aviso
        # lateral y no debe tumbar la importacion de fichas que lo invoca.
        pass
