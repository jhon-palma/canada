"""Envio de avisos por correo.

Hay dos remitentes y no es casualidad: los avisos tecnicos -- que la
importacion de fichas termino, que la descarga de videos fallo -- salen de una
cuenta y van al buzon de soporte, y los avisos de negocio salen de la cuenta de
LJ. Quien llama elige pasando el remitente, y aqui se busca con que credenciales
enviar.

Antes las dos cuentas estaban escritas en este archivo, con sus dos contrasenas
de aplicacion de Gmail, y ademas DEBUG se colaba en la condicion: con DEBUG
encendido todo salia por la cuenta de soporte y se desviaba a su buzon. Eso
ultimo es util en desarrollo, pero es una decision propia y ahora se dice con
EMAIL_REDIRECT_TO en vez de deducirse de si Django esta depurando.
"""

import smtplib
from email.mime.text import MIMEText

from django.conf import settings


def _credenciales(sender):
    """La cuenta con la que enviar, segun quien figure como remitente."""
    if sender and sender.strip().lower() == settings.EMAIL_ALERTS_USER.strip().lower():
        return settings.EMAIL_ALERTS_USER, settings.EMAIL_ALERTS_PASSWORD
    return settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD


def sendEmail(sender, destinatary, subject, content):
    usuario, contrasena = _credenciales(sender)
    if not usuario or not contrasena:
        return

    # Puesto, todo el correo va ahi en vez de a su destinatario. Es para
    # desarrollo; en produccion se deja vacio.
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
        # Se traga el fallo a proposito, como antes: el aviso es lateral y no
        # debe tumbar la importacion de fichas que lo invoca.
        pass
