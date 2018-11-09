
# coding: utf-8

# from distutils.core import setup
from setuptools import setup
setup(
    name='tmtk',
    version='1.0.5',
    description='Traditional Mongolian ToolKit',
    author='Aronsoyol',
    author_email='aronsoyol@gmail.com',
    url='git@gitlab.com:aronsoyol/tmtk.git',
    install_requires=[
        'freetype-py',
        'numpy',
        'pillow',
        'imagehash',
        'pygobject'],
    packages=['tmtk', 'tmtk.__utils'],
    include_package_data=True,
    package_data={'tmtk': [
        'MongolianWhite3.ttf',
        'dictionary_garray.jl',
        'gid_2_hash.json']},
    test_suite='test'
)
