#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


def web_images_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    name = '{}{}'.format(instance.reference, ext)
    return 'public/web/images/{}'.format(name)
