
# coding: utf-8

# from distutils.core import setup
from setuptools import setup
setup(
    name='tmtpk',
    version='1.0.4',
    description='Traditional Mongolian Text Processing Kit',
    author='Aronsoyol',
    author_email='aronsoyol@gmail.com',
    url='https://github.com/aronsoyol/tmtpk',
    install_requires=[
        'freetype-py',
        'numpy',
        'pillow',
        'imagehash',
        'pygobject'],
    packages=['tmtpk'],
    include_package_data=True,
    package_data={'tmtpk': ['MongolianWhite3.ttf', 'dictionary_garray.jl']},
    test_suite='test'
)
