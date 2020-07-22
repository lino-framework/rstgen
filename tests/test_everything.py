# -*- coding: UTF-8 -*-

from atelier.test import TestCase

class BasicTests(TestCase):

    def test_01(self):
        self.assertEqual(1+1, 2)

    def test_readme(self):
        self.run_simple_doctests('README.rst')

    def test_rstgen(self):
        self.run_simple_doctests('rstgen/__init__.py')
    def test_rstgen(self):
        self.run_simple_doctests('rstgen/utils.py')
