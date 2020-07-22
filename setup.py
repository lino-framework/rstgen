from setuptools import setup

SETUP_INFO = dict(
    name='rstgen',
    version='20.7.1',
    packages=['rstgen'],
    install_requires=[],
    test_suite='tests',
    description="Generate rst chunks from Python objects.",
    license='BSD-2-Clause',
    author='Luc Saffre',
    author_email='luc.saffre@gmail.com')

SETUP_INFO.update(classifiers="""\
Programming Language :: Python
Programming Language :: Python :: 3
Development Status :: 5 - Production/Stable
Intended Audience :: Developers
License :: OSI Approved :: BSD License
Natural Language :: English
Operating System :: OS Independent""".splitlines())

SETUP_INFO.update(long_description=open("README.rst").read())

if __name__ == '__main__':
    setup(**SETUP_INFO)
