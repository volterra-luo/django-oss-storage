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
        # entry is a tuple of
        # (object_key, last_modified, etag, size, owner.id, owner.display_name, storage_class)
        if self.preload_metadata and not self._entries:
            res = self.connection.list_bucket(self.bucket, self.prefix, 
                    self.marker, self.delimiter, self.maxkeys, self.headers)
            
            if (res.status / 100) == 2:
                body = res.read()
                h = GetBucketXml(body)
                (file_list, common_list) = h.list()
                self._entries = dict((entry[0], entry) for entry in file_list)
        
        return self._entries
	
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

        if self.encrypt:
            pass

        content_type = mimetypes.guess_type(name)[0] or "application/x-octet-stream"

        if self.gzip and content_type in self.gzip_content_types:
            content = self._compress_string(content)
            self.headers.update({'Content-Encoding': 'gzip'})

        self.headers.update({
            'x-oss-acl': self.acl,
            'Content-Type': content_type,
            'Content-Length' : str(len(content)),
        })
        res = self.connection.put_object_from_string(self.bucket, name, content, content_type, self.headers)
        if res.status not in (200, 206):
            raise IOError("OssStorageError: %s" % res.read())

    def _open(self, name, mode='rb'):
        '''_open should return a subclass of Django File object'''
        name = self._clean_name(name)
        remote_file = OssStorageFile(name, self, mode=mode)
        return remote_file

    def _read(self, name, start_range=None, end_range=None):
        pass

    def _save(self, name, content):
        name = self._clean_name(name)
        content.open()
        if hasattr(content, 'chunks'):
            content_str = ''.join(chunk for chunk in content.chunks())
        else:
            content_str = content.read()
        self._put_file(name, content_str)
        return name

    def delete(self, name):
        name = self._clean_name(name)
        res = self.connection.delete_object(self.bucket, name)
        if res.status != 204:
            raise IOError("OssStorageError: %s" % res.read())

    def exists(self, name):
        name = self._clean_name(name)
        if self.entries:
            return name in self.entries
        res = self.connection.head_object(self.bucket, name)
        return res.status == 200

    def listdir(self, path):
        pass

    def size(self, name):
        name = self._clean_name(name)
        if self.entries:
            entry = self.entries.get(name)
            if entry:
                return int(entry[3])
            return 0
        
        res = self.connection.head_object(self.bucket, name, self.headers)
        if (res.status / 100) == 2:
            header_map = convert_header2map(res.getheaders())
            content_length = safe_get_element("content-length", header_map)
        
        return content_length and int(content_length) or 0

    def url(self, name):
        name = self._clean_name(name)
        if self.base_url is None:
            raise ValueError("This file is not accessible via a URL.")
        return urljoin(self.base_url, filepath_to_uri(name))

    def modified_time(self, name):
        try:
           from dateutil import parser, tz
        except ImportError:
            raise NotImplementedError()
        name = self._clean_name(name)
        if self.entries:
            last_modified = self.entries.get(name)[1]
        else:
            res = self.connection.head_object(self.bucket, name)
            header_map = convert_header2map(res.getheaders())
            last_modified = safe_get_element('Last-Modified', header_map)
            last_modified = unicode(last_modified)
        
        # convert to string to date
        last_modified_date = parser.parse(last_modified)
        # if the date has no timzone, assume UTC
        if last_modified_date.tzinfo == None:
            last_modified_date = last_modified_date.replace(tzinfo=tz.tzutc())
        # convert date to local time w/o timezone
        return last_modified_date.astimezone(tz.tzlocal()).replace(tzinfo=None) 

class OssStorageFile(File):
    """OssStorageFile is a File object that 
        implements logic specific for OSS backend storage system"""

    def __init__(self, name, storage, mode):
        self._name =  name
        self._storage = storage
        self._mode = mode
        self._is_dirty = False
        self.file = StringIO()
        self.start_range = 0

		
if __name__=='__main__':
	pass
