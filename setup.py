from setuptools import setup
from setuptools import find_packages

setup(
    name='srdotcomScraper',
    version='0.0.1', 
    description='',
    url='https://github.com/GuhCH/data-collection-pipeline',
    author='Joe Gocher',
    license='MIT',
    packages=find_packages(),
    install_requires=['selenium', 'uuid', 'requests', 'time', 'typing', 'json', 're'],
)