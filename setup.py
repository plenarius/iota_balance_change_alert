#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'pyota>=2.0',
    'schedule>=0.5.0',
    'ConfigParser;python_version<"3"',
    'configparser;python_version>="3"',
]

setup_requirements = [
    # TODO(plenarius): put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='iota_balance_change_alert',
    version='0.1.1',
    description="IOTA Balance Change Alert checks the balance on one or more addresses at a specified interval and alerts the user if there's any change in balance.",
    long_description=readme + '\n\n' + history,
    author="James Greenhalgh",
    author_email='plenarius@gmail.com',
    url='https://github.com/plenarius/iota_balance_change_alert',
    packages=find_packages(include=['iota_balance_change_alert']),
    entry_points={
        'console_scripts': [
            'iota_balance_change_alert=iota_balance_change_alert.cli:main'
        ]
    },
    include_package_data=True,
    data_files=[('config', ['config.ini.example'])],
    install_requires=requirements,
    extras_require={'Twilio': ["twilio>0.6"],},
    license="MIT license",
    zip_safe=False,
    keywords='iota_balance_change_alert',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
