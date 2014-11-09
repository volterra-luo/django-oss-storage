#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import django

BASE_PATH = os.path.dirname(__file__)

def main():

	os.environ["DJANGO_SETTINGS_MODULE"] = "django.conf.global_settings"
	from django.conf import global_settings

	global_settings.INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.sessions',
        'django.contrib.contenttypes',
        'storages',
    )

    global_settings.DATABASES = {
    	'default': {
    		'ENGINE': 'django.db.backends.sqlite3',
    		'NAME': os.path.join(BASE_PATH, 'tests.sqlite'),
    		'USER': '',
    		'PASSWORD': '',
    		'HOST': '',
    		'PORT': '',
    	}

    global_settings.DEFAULT_FILE_STORAGE = 'backends.s3boto.S3BotoStorage'

	from django.test.utils import get_runner
	test_runner = get_runner(global_settings)

if __name__ == '__main__':
	main()