#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'six',
    'psutil>=2.0',
]

# bundled actions
entry_points = {
    'nrtest.compare': [
        'default=nrtest.compare:default_compare',
        'null=nrtest.compare:null_compare',
    ]
}

setup(
    name='nrtest',
    version='0.2.2',
    description="Numerical regression testing",
    long_description=readme + '\n\n' + history,
    author="David Hall",
    author_email='dhcrawley@gmail.com',
    url='https://github.com/davidchall/nrtest',
    packages=[
        'nrtest',
    ],
    scripts=[
        'scripts/nrtest',
    ],
    entry_points=entry_points,
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='nrtest',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests'
)
