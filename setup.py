#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'requests>=2.0.0',
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='pycofecms',
    version='0.1.0',
    description='Church of England CMS API Client',
    long_description=readme + '\n\n' + history,
    author='Blanc Ltd.',
    author_email='studio@blanc.ltd.uk',
    url='https://github.com/blancltd/pycofecms',
    packages=[
        'pycofecms',
    ],
    package_dir={'pycofecms':
                 'cofecms'},
    include_package_data=True,
    install_requires=requirements,
    license='BSD license',
    zip_safe=False,
    keywords='cofecms',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
