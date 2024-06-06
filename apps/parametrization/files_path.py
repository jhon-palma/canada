#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from apps.parametrization.utils import remove_spaces


def company_path(instance, filename):
    name = remove_spaces(filename, r'\s+')
    dir = 'companys/photos/{}'.format(name)
    return dir


def entity_path(instance, filename):
    name = remove_spaces(filename, r'\s+')
    dir = 'entitys/photos/{}'.format(name)
    return dir


def type_alert_path(instance, filename):
    name = remove_spaces(filename, r'\s+')
    dir = 'type_alerts/photos/{}'.format(name)
    return dir