#!/usr/bin/env python3

import os

from typing import List

from setuptools import setup, find_packages


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def read_list(file_path):
    if not os.path.isfile(file_path):
        return []
    ret_list = []
    with open(file_path, "r", encoding="utf-8") as content_file:
        for line in content_file:
            if line.startswith("git"):
                ## skip -- setuptools does not support installing packages from git remote repo
                continue
            ret_list.append(line.strip())
    return ret_list


packages_list = find_packages(include=["mpyserialprotogen", "mpyserialprotogen.*"])

## additional data to install
packages_data = {
    "mpyserialprotogen": [
        "*.txt",
        "template/*.tmpl",
        "template/*.texhon",
        "template/**/*.tmpl",
        "template/**/*.texhon",
        "template/*.py",
        "template/**/*.py",
    ]
}

## additional scripts to install
additional_scripts: List[str] = []

requirements_path = os.path.join(SCRIPT_DIR, "requirements.txt")
install_reqs = read_list(requirements_path)
install_reqs.extend([])  # additional packages to install

## every time setup info changes then version number should be increased

setup(
    name="mpyserialprotogen",
    version="1.0.1",
    description="Generate message exchange protocol layer for MicroPython",
    url="https://github.com/anetczuk/mpython-serial-protogen",
    author="anetczuk",
    license="BSD 3-Clause",
    packages=packages_list,
    package_data=packages_data,
    scripts=additional_scripts,
    install_requires=install_reqs,
)
