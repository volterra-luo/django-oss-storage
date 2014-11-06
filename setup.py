#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import storages.pkg_info

exclude = ["*.tests", "*.tests.*", "tests.*", "tests"]

setup(
    name = storages.pkg_info.package,
    version = storages.pkg_info.version,
    packages = find_packages(exclude),
    author = 'volterra-luo',
    author_email = 'volterra-luo@aliyun.com',
    url = storages.pkg_info.url,
    description = storages.pkg_info.short_description,
    long_description = open('README.md').read(),
    license = storages.pkg_info.license,
    requires = [
        'Django',
        'python-dateutil>=2.2',
    ],
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: System :: Installation/Setup'
    ],
    zip_safe = False
    test_suite = 'storages.tests.main'
)