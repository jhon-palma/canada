#!/usr/bin/env python
# -*- coding: utf-8 -*-

import boto3
from storages.backends.s3boto3 import S3Boto3Storage
from botocore.exceptions import ClientError


class StaticStorage(S3Boto3Storage):
    location = 'static'
    default_acl = 'public-read'


class MediaStorage(S3Boto3Storage):
    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False


