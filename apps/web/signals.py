#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from ..vars import *
from .utils import *
from .dicts import *
import random


"""
@receiver(pre_save, sender=WebPQR)
def pre_save_web_pqr(sender, instance, **kwargs):
    instance.color = PQR_STATUS_COLOR.get(instance.status)
"""
