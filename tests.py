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

	from django.test.utils import get_runner
	test_runner = get_runner(global_settings)

if __name__ == '__main__':
	main()