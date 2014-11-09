#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys


BASE_PATH = os.path.dirname(__file__)

from django.test import TestCase


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)