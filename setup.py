import os
from setuptools import setup, find_packages

def get_version():
    basedir = os.path.dirname(__file__)
    with open(os.path.join(basedir, 'r2drink2/version.py')) as f:
        __version__ = None
        exec(f.read())
        return __version__

setup(
    name='r2drink2',
    version=get_version(),
    packages=find_packages(),
    install_requires=[],
    include_package_data=True
)
