#!/usr/bin/env python
# -*- coding:utf-8 -*-
from distutils.core import setup
import os

# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir:
    os.chdir(root_dir)

for dirpath, dirnames, filenames in os.walk('temporale'):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        pkg = dirpath.replace(os.path.sep, '.')
        if os.path.altsep:
            pkg = pkg.replace(os.path.altsep, '.')
        packages.append(pkg)
    elif filenames:
        prefix = dirpath[13:] # Strip "registration/" or "registration\"
        for f in filenames:
            data_files.append(os.path.join(prefix, f))


setup(name='fiee-temporale',
      version='0-0-0',
      description=u'Generic events for your django models',
      author='Henning Hraban Ramm',
      author_email='hraban@fiee.net',
      url='https://github.com/fiee/fiee-temporale',
      download_url='https://github.com/fiee/fiee-temporale/tarball/master',
      package_dir={'temporale': 'temporale'},
      packages=packages,
      package_data={'temporale': data_files},
      # see http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=['Development Status :: 2 - Pre-Alpha',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   'Topic :: Utilities',
                   'Natural Language :: English',
                   'Natural Language :: German'],
      install_requires=['Django>=1.2', 'django-registration', 'fiee-dorsale'],
      )
