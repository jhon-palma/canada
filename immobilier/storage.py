#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class MediaS3Boto3Storage(S3Boto3Storage):
    file_overwrite = True

    def _save(self, name, content):
        public_directories = ['public/', 'public\\']
        if any(directory in name for directory in public_directories):
            self.default_acl = 'public-read'
        else:
            self.default_acl = 'private'

        return super()._save(name, content)


