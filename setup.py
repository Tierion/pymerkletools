import os

from setuptools import find_packages
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))


setup(
    name='merkle_tools',
    version='1.0.0',
    description='Merkle Tools',
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
    ],
    url='https://github.com/',
    author='Eder Santana',
    keywords='merkle tree, blockchain, tierion',
    license="MIT",
    packages=find_packages(),
        include_package_data=False,
        zip_safe=False,
)
