from setuptools import setup

SETUP_INFO = dict(
    name='rstgen',
    version='22.6.0',
    packages=['rstgen', 'rstgen.sphinxconf', 'rstgen.sphinxconf.languages'],
    install_requires=[],
    tests_require=['atelier'],
    test_suite='tests',
    description="Pythonic API for generating reStructuredText.",
    license_files=['COPYING'],
    url='https://github.com/lino-framework/rstgen',
    author='Luc Saffre',
    author_email='luc.saffre@gmail.com')

SETUP_INFO.update(classifiers="""\
Programming Language :: Python
Programming Language :: Python :: 3
Development Status :: 5 - Production/Stable
Intended Audience :: Developers
License :: OSI Approved :: GNU Affero General Public License v3
Natural Language :: English
Operating System :: OS Independent""".splitlines())

SETUP_INFO.update(long_description=open("README.rst").read())

SETUP_INFO.update(
    zip_safe=False,
    include_package_data=True)



if __name__ == '__main__':
    setup(**SETUP_INFO)
