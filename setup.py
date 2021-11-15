#!/usr/bin/env python3

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tv_tools",
    version="0.1.1",
    author="Fabrice Quenneville",
    author_email="fab@fabq.ca",
    url="https://github.com/fabquenneville/tv_tools",
    download_url="https://pypi.python.org/pypi/tv_tools",
    project_urls={
        "Bug Tracker": "https://github.com/fabquenneville/tv_tools/issues",
        "Documentation": "https://fabquenneville.github.io/tv_tools/",
        "Source Code": "https://github.com/fabquenneville/tv_tools",
    },
    description="tv_tools is a Python command line tool to manage a media database.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Topic :: Multimedia :: Video :: Conversion",
        "Development Status :: 5 - Production/Stable",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    entry_points = {
        'console_scripts': ['tv_tools=tv_tools.tv_tools:main'],
    },
    keywords=[
        "media-database", "python-command"
    ],
    install_requires=[
        "pathlib","colorama"
    ],
    license='GPL-3.0',
    python_requires='>=3.6',
    test_suite='nose.collector',
    tests_require=['nose'],
    zip_safe=True,
)