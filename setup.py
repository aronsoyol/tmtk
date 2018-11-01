
# coding: utf-8

#!/usr/bin/env python

from distutils.core import setup

setup(name='timu',
      version='1.0',
      description='Traditional Mongolian Word Unifer',
      author='Aronsoyol',
      author_email='aronsoyol@gmail.com',
      url='https://github.com/aronsoyol/timu',
      install_requires=['freetype-py',
                        'numpy',
                        'pillow',
                        'imagehash',
                        'pygobject'],
      packages=['timu'],
      )
