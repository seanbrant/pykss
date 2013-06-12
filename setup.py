#!/usr/bin/env python
from setuptools import setup, find_packages


setup(
    name='pykss',
    version='0.4',
    description='Python implementation of KSS',
    long_description=open('README.rst').read(),
    author='Sean Brant',
    author_email='brant.sean@gmail.com',
    url='https://github.com/seanbrant/pykss',
    license='BSD',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    zip_safe=False,
    test_suite='runtests.runtests',
    extras_require={
        'tests': [
            'Django>=1.5',
            'flake8',
            'mock',
            'pytest',
        ],
    },
)
