# -*- coding: UTF-8 -*-

from atelier.test import TestCase

class BasicTests(TestCase):

    def test_readme(self):
        self.run_simple_doctests('README.rst')
    def test_rstgen(self):
        self.run_simple_doctests('rstgen/__init__.py')
    def test_rstgen(self):
        self.run_simple_doctests('rstgen/utils.py')

class SphinxTests(TestCase):
    def test_sphinxconf(self):
        self.run_simple_doctests('rstgen/sphinxconf/__init__.py')

    def test_base(self):
        self.run_simple_doctests('rstgen/sphinxconf/base.py')

    def test_sigal(self):
        self.run_simple_doctests('rstgen/sphinxconf/sigal_image.py')
