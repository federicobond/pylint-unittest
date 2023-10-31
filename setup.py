# coding: UTF-8

import os

from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='pylint-unittest',
    url='https://github.com/federicobond/pylint-unittest',
    author='Federico Bond',
    author_email='federicobond@gmail.com',
    description='A Pylint plugin for detecting incorrect use of unittest assertions',
    long_description=read('README.rst'),
    version='0.2.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pylint',
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    license='GPLv3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: Unix',
        'Topic :: Software Development :: Quality Assurance',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    keywords=['pylint', 'unittest', 'plugin'],
)
