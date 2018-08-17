from setuptools import setup, find_packages


MAJOR = 0
MINOR = 0
MICRO = 4

VERSION = '{}.{}.{}'.format(MAJOR, MINOR, MICRO)


setup(
  name='sixer',
  version=VERSION,
  description='Python 2/3 compatibility linter',
  author='Taylor Jackle Spriggs',
  author_email='fndasltn@gmail.com',
  url='https://github.com/taylorjacklespriggs/sixer',
  packages=find_packages(),
  scripts=[
    'bin/sixer',
  ]
)
