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
    version='0.1.1',
    description='Church of England CMS API Client',
    long_description=readme + '\n\n' + history,
    author='The Developer Society',
    author_email='studio@dev.ngo',
    url='https://github.com/developersociety/pycofecms',
    python_requires='>=3.5',
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
