# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

from distutils.core import setup
from setuptools import find_packages

from mutagenerate import __version__ as mutagenerate_version

setup(
    name='mutagenerate',
    version='.'.join(map(str, mutagenerate_version)),
    author='Guillaume Thomas',
    author_email='guillaume.thomas642@gmail.com',
    license='LICENCE.txt',
    description="Mutagenerate is a python module which tries to extend as much as possible id3 tags based on tags already set and public web resources",
    url='https://github.com/gtnx/mutagenerate',
    install_requires=map(
        lambda line: line.strip("\n"),
        open("requirements.txt", "r").readlines()
    ),
    include_package_data=True,
    packages=find_packages(),
    scripts=('bin/mid3generate.py', 'bin/mid3ls', 'bin/mid3cover'),
)
