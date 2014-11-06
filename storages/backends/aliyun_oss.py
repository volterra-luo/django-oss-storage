#!/usr/bin/env python
# -*- coding:utf-8 -*-

# The MIT License (MIT)

# Copyright (c) 2014 volterra-luo

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


'''
Django Storage Backend for Aliyun Open Storage Service(OSS).
'''

import os
import mimetypes
import warnings

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from django.conf import settings
from django.core.files.base import File
from django.core.files.storage import Storage
from django.core.exceptions import ImproperlyConfigured
from django.utils.deconstruct import deconstructible
from django.utils.encoding import force_text, filepath_to_uri
from django.utils.six.moves.urllib.parse import urljoin

try:
    from oss.oss_api import OssAPI
    from oss.oss_xml_handler import GetServiceXml, GetBucketAclXml, GetBucketXml
    from oss.oss_util import convert_header2map, safe_get_element
except ImportError:
    raise ImproperlyConfigured("未能导入Aliyun OSS SDK.\n参见 "
        "http://help.aliyun.com/view/13438815.html?spm=5176.383663.9.4.jfQkJZ")

OSS_HOST 			= getattr(settings, 'OSS_HOST', "oss.aliyuncs.com")
ACCESS_KEY_NAME     = getattr(settings, 'OSS_ACCESS_KEY_ID', getattr(settings, 'ACCESS_KEY_ID', None))
SECRET_KEY_NAME     = getattr(settings, 'OSS_SECRET_ACCESS_KEY', getattr(settings, 'SECRET_ACCESS_KEY', None))
HEADERS             = getattr(settings, 'OSS_HEADERS', {})
DEFAULT_ACL         = getattr(settings, 'DEFAULT_ACL', 'private')

BUCKET_PREFIX       = getattr(settings, 'BUCKET_PREFIX', '')
PRELOAD_METADATA    = getattr(settings, 'PRELOAD_METADATA', False)

IS_GZIPPED          = getattr(settings, 'IS_GZIPPED', False)
GZIP_CONTENT_TYPES  = getattr(settings, 'GZIP_CONTENT_TYPES', (
    'text/css',
    'application/javascript',
    'application/x-javascript'
))

if IS_GZIPPED:
    from gzip import GzipFile

class OssStorage(Storage):
	"""Aliyun OSS Storage Service"""
	def __init__(self, bucket=settings.OSS_STORAGE_BUCKET_NAME,
                access_key=None, secret_key=None, base_url=settings.MEDIA_URL, 
                acl=DEFAULT_ACL, encrypt=False, prefix = BUCKET_PREFIX, 
                gzip=IS_GZIPPED, gzip_content_types=GZIP_CONTENT_TYPES,
                preload_metadata=PRELOAD_METADATA
            ):
		super(OssStorage, self).__init__()
		self.bucket = bucket
        self.acl = acl
        self.encrypt = encrypt
        self.gzip = gzip
        self.gzip_content_types = gzip_content_types
        self.preload_metadata = preload_metadata
        self.base_url = base_url

        if encrypt:
        	pass

        if not access_key and not secret_key:
            access_key, secret_key = self._get_access_keys()

        self.connection = OssAPI(OSS_HOST, access_key, secret_key)

        self.prefix = prefix
        self.marker = ''
        self.delimiter = ''
        self.maxkeys = ''
        self.headers = HEADERS
        self._entries = {}

    def _get_access_keys(self):
        access_key = ACCESS_KEY_NAME
        secret_key = SECRET_KEY_NAME
        # only provided access_key or only provided secret_key
        if (access_key or secret_key) and (not access_key or not secret_key):
            access_key = os.environ.get(ACCESS_KEY_NAME)
            secret_key = os.environ.get(SECRET_KEY_NAME)

        if access_key and secret_key:
            # Both were provided, so use them
            return access_key, secret_key

        return None, None

    @property
    def entries(self):
        pass
	
    def _clean_name(self, name):
        # Useful for windows' paths
        return os.path.join(BUCKET_PREFIX, os.path.normpath(name).replace('\\', '/'))

    def _compress_string(self, s):
        """Gzip a given string."""
        zbuf = StringIO()
        zfile = GzipFile(mode='wb', compresslevel=6, fileobj=zbuf)
        zfile.write(s)
        zfile.close()
        return zbuf.getvalue()

    def _put_file(self, name, content):
        pass


	def _open(self, name, mode='rb'):
		pass

    def _read(self, name, start_range=None, end_range=None):
        pass
        

	def _save(self, name, content):
		pass

	def delete(self, name):
        pass

	def exists(self, name):
       pass

	def listdir(self, path):
       pass

	def size(self, name):
		pass
        
       

	def url(self, name):
        name = self._clean_name(name)
        if self.base_url is None:
            raise ValueError("This file is not accessible via a URL.")
        return urljoin(self.base_url, filepath_to_uri(name))

    
    def modified_time(self, name):
        pass

class OssStorageFile(File):
    """OssStorageFile is a File object that 
        implements logic specific for OSS backend storage system"""
    pass

		
if __name__=='__main__':
	pass
