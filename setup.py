
# coding: utf-8

# from distutils.core import setup
from setuptools import setup
      install_requires=['freetype-py',
                        'numpy',
                        'pillow',
                        'imagehash',
                        'pygobject'],
      packages=['timu'],
      include_package_data=True,
      package_data={'timu': ['MongolianWhite3.ttf']},
      )
