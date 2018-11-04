
# coding: utf-8

# from distutils.core import setup
from setuptools import setup
setup(
    name='timu',
    version='1.0.2',
    description='Traditional Mongolian Word Unifer',
    author='Aronsoyol',
    author_email='aronsoyol@gmail.com',
    url='https://github.com/aronsoyol/timu',
    install_requires=[
        'freetype-py',
        'numpy',
        'pillow',
        'imagehash',
        'pygobject'],
    packages=['timu'],
    include_package_data=True,
    package_data={'timu': ['MongolianWhite3.ttf']},
    test_suite='test'
)
