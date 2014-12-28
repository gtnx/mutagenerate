from distutils.core import setup
from setuptools import find_packages

setup(name='mutagenerate',
      version='0.1.3',
      author='Guillaume Thomas',
      author_email='guillaume.thomas642@gmail.com',
      license='LICENCE.txt',
      description="Mutagenerate is a python module which tries to extend as much as possible id3 tags based on tags already set and public web resources",
      url='https://github.com/gtnx/mutagenerate',
      install_requires=map(lambda line: line.strip("\n"),
                           open("requirements.txt", "r").readlines()),
      include_package_data=True,
      packages=find_packages(),
      scripts=('bin/mid3generate.py', ),
      )
