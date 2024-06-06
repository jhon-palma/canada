#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
from datetime import datetime, timedelta, date
from celery import task
from config.celery import app
from config.settings import *
from apps.vars import *
import time, os, requests, json, re


"""
@app.task()
def notification_administrative(title, content, recipient, telegram_chat):
"""