"""Setup configuration for Password Vault package."""

from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="password-vault",
    version="1.0.0",
    author="Tharun Ponnam",
    author_email="tharunponnam007@gmail.com",
    description="A secure local password management application with GUI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tharun-ship-it/password-vault",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Security",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "password-vault=src.vault:main",
        ],
    },
)
