#!/usr/bin/env python
# -*- coding:utf-8 -*-
from setuptools import setup, find_packages
import os

setup(name='fiee-temporale',
      version='0.0.2a1',
      description=u'Generic events for your django models',
      keywords='event date calendar generic attachment',
      author='Henning Hraban Ramm',
      author_email='hraban@fiee.net',
      license='BSD',
      url='https://github.com/fiee/fiee-temporale',
      download_url='https://github.com/fiee/fiee-temporale/tarball/master',
      package_dir={'temporale': 'temporale',},
      packages=find_packages(),
      include_package_data = True,
      package_data = {'': ['*.rst', 'locale/*/LC_MESSAGES/*.*', 'templates/*/*.*', 'templates/*/*/*.*', ]},
      # see http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=['Development Status :: 3 - Alpha',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   'Topic :: Utilities',
                   'Natural Language :: English',
                   'Natural Language :: German',],
      install_requires=['Django>=1.6', 'vobject', 'django-registration', 'fiee-dorsale',],
      zip_safe=False,
      )
