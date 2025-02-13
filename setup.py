from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="blackjack-simulator",
    version="0.1.0",
    author="Ardeshir",
    author_email="a.damavandi@hotmail.com",
    description="A sophisticated Blackjack game simulator with multiple strategies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ardeshir21/blackjack-simulator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Games/Entertainment",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pandas>=1.3.0",
        "numpy>=1.21.0",
        "matplotlib>=3.4.0",
        "openpyxl>=3.0.0",
    ],
    extras_require={
        'dev': [
            'pytest>=6.2.5',
            'pytest-cov>=2.12.0',
            'black>=21.5b2',
            'flake8>=3.9.2',
        ],
    },
    entry_points={
        'console_scripts': [
            'blackjack=src.game.blackjack:main',
        ],
    },
) 