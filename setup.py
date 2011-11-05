import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
    
setup(
    name="knife",
    version="0.1.0",
    description="Dynamic HTML without a Template DSL",
    author="Chip Tol",
    author_email="wiremine@gmail.com",
    package_dir={'': 'src'},
    packages=['knife'],
    license="MIT",
    test_suite='knife',
    classifiers = (
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6"
    )
)    