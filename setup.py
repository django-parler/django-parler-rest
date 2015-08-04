#!/usr/bin/env python
from setuptools import setup, find_packages
from os import path
import codecs
import re
import sys
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]
    DEFAULT_PYTEST_ARGS = "-vvv --cov parler_rest --cov-report html testproj"

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.pytest_args or self.DEFAULT_PYTEST_ARGS)
        sys.exit(errno)


def read(*parts):
    file_path = path.join(path.dirname(__file__), *parts)
    return codecs.open(file_path, encoding='utf-8').read()


def find_version(*parts):
    version_file = read(*parts)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return str(version_match.group(1))
    raise RuntimeError("Unable to find version string.")


setup(
    name='django-parler-rest',
    version=find_version('parler_rest', '__init__.py'),
    license='Apache 2.0',

    install_requires=[
        'django-parler>=1.2',
        'djangorestframework>=3.0',
    ],
    requires=[
        'Django (>=1.4.2)',
    ],
    tests_require=[
        'django>=1.8',
        'six==1.9.0',
        'pytest==2.7.1',
        'pytest-django==2.8.0',
        'pytest-cov==1.8.1',
    ],
    cmdclass={'test': PyTest},

    description='Multilingual support for django-rest-framework',
    long_description=read('README.rst'),

    author='Diederik van der Boor',
    author_email='opensource@edoburu.nl',

    url='https://github.com/edoburu/django-parler-rest',
    download_url='https://github.com/edoburu/django-parler-rest/zipball/master',

    packages=['parler_rest'],
    include_package_data=True,

    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3.2',
        # 'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
