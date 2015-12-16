#!/usr/bin/env python

from django.conf import settings
from django.core.management import execute_from_command_line
import django
import os
import sys

if not settings.configured:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testproj.settings")
    if django.VERSION >= (1, 7):
        django.setup()
    module_root = os.path.dirname(os.path.realpath(__file__))
    sys.path.insert(0, module_root)


def runtests():
    argv = sys.argv[:1] + ['test', 'testproj'] + sys.argv[1:]
    execute_from_command_line(argv)


if __name__ == '__main__':
    runtests()
