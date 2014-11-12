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
	
    def test_storage_save(self):
        """
        Test saving a file
        """
        name = 'test_storage_save.txt'
        content = ContentFile('new content')
        self.storage.save(name, content)
        self.storage.bucket.get_key.assert_called_once_with(name)
        
        key = self.storage.bucket.get_key.return_value
        key.set_metadata.assert_called_with('Content-Type', 'text/plain')
        key.set_contents_from_file.assert_called_with(
            content,
            headers={},
            policy=self.storage.acl,
            reduced_redundancy=self.storage.reduced_redundancy,
        )



class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)