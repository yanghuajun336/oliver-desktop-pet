"""Setup script for packaging"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip()]

setup(
    name="oliver-desktop-pet",
    version="0.1.0",
    author="Yang Huajun",
    author_email="",
    description="Oliver - Star Scholar Owl Desktop Pet for Windows",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yanghuajun336/oliver-desktop-pet",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: Microsoft :: Windows :: Windows 11",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Games/Entertainment",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "oliver=src.main:main",
        ],
    },
)
