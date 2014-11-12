#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

import mock
from uuid import uuid4
from urllib2 import urlopen

from django.test import TestCase
from django.core.files.base import ContentFile
from django.conf import settings
from django.core.files.storage import FileSystemStorage


from storages.backends import aliyun_oss


class AliyunOssTestCase(TestCase):
    @mock.patch('')
    def setUp(self):
        self.storage = aliyun_oss.S3BotoStorage()

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)