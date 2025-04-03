#!/usr/bin/env python3
"""
Setup script for the RecursiveDevKit framework.
"""

from setuptools import setup, find_packages

setup(
    name="recursive-devkit",
    version="0.1.0",
    description="A framework for AI-assisted recursive software development",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/recursive-devkit",
    packages=find_packages(),
    py_modules=["recursive_devkit"],
    entry_points={
        "console_scripts": [
            "recursive-devkit=recursive_devkit:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
)
