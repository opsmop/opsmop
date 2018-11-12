#!/usr/bin/env python

from distutils.core import setup

setup(name='opsmop',
      version='0.1',
      description='elite configuration management',
      author='Michael DeHaan',
      author_email='michael@michaeldehaan.net',
      url='https://opsmop.io/',
      packages=['opsmop'],
      scripts=['bin/opsmop']
     )
