# Copyright (c) 2010 Guilherme Gondim and contributors
#
# This file is part of Django Admin Help.
#
# Django Admin Help is free software under terms of the GNU Lesser
# General Public License version 3 (LGPLv3) as published by the Free
# Software Foundation. See the file README for copying conditions.

"""
**Django Admin Help** is a pluggable help system for `Django Web Framework`_
to be used with administration application.

Admin Help was inspired by help system of `Django Grappelli`_.

..
  _`Django Web Framework`: http://www.djangoproject.com
  _`Django Grappelli`: http://django-grappelli.googlecode.com

"""

VERSION = (0, 1)

def get_version():
    """
    Returns the version as a human-format string.
    """
    return '.'.join([str(i) for i in VERSION])

__author__ = 'See the file AUTHORS.'
__license__ = 'GNU Lesser General Public License (GPL), Version 3'
__url__ = 'http://github.com/semente/django-adminhelp'
__version__ = get_version()
