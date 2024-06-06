#!/usr/bin/env python
# -*- coding: utf-8 -*-


TYPE_REQUEST_CONTRACT_PROPERTY_CHOICES = (
    ('sale','Vender'),
    ('rent','Alquilar'),
    ('buy','Comprar'),
)


TYPE_REQUEST_PROPERTY_CHOICES = (
    ('search','Solicitud de Búsqueda'),
    ('acm','Solicitud de ACM'),
)


TYPE_REQUEST_CHOICES = (
    ('query','Consulta'),
    ('claim','Reclamo'),
    ('property','Sobre tu Propiedad'),
    ('other','Otro Motivo'),
)


STATUS_PQR_CHOICES = (
    ('no_attend','Sin Resolver'),
    ('office','Asignada a Oficina'),
    ('attend','Resuelta'),
    ('discarded','Descartada'),
)


STATUS_INTERESTED_PROPERTY_CHOICES = (
    ('no_attend','Sin Atender'),
    ('office','Asignado a Oficina'),
    ('attend','Atendido'),
    ('discarded','Descartado'),
)


STATUS_INTERESTED_FRANCHISE_CHOICES = (
    ('no_contact','No Contactado'),
    ('contact','Contactado'),
    ('discarded','Descartado'),
)

STATUS_PROSPECT_CHOICES = (
    ('no_attend','Sin Asignar'),
    ('office','Asignado a Oficina'),
    ('afiliate','Afiliado'),
    ('process','En Proceso'),
    ('discarded','Descartado'),
)


EXPERIENCE_CHOICES = (
    ('no','Ninguna'),
    ('basic','Básica'),
    ('medium','Intermedia'),
    ('all','Total'),
)


WEB_CHOICES = (
    ('online','Publicidad Online'),
    ('letter','Aviso Clasificado'),
    ('google','Buscadores (Google)'),
    ('propertie','Carte en una Propiedad'),
    ('office','Catalogo de Franquicias'),
    ('asesor','Por medio de un Asesor Re/max'),
    ('via','Publicidad en Via Publica'),
)