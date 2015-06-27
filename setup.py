from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup


__version__ = '0.1b0'


setup(
    name='babydbcli',
    version=__version__,
    description='little Dropbox CLI',
    scripts=['scripts/bdb'],
    install_requires=[
        'dropbox>=2.2.0',
    ],
    url='https://github.com/cjmay/babydbcli',
    license='BSD',
)
