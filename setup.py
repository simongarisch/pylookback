from setuptools import setup, find_packages


setup(
    name="pylookback",
    version="0.1.0",

    author="Simon Garisch",
    author_email="gatman946 at gmail.com",

    description="An event driven backtester using only the standard library.",
    long_description=open("README.md").read(),

    packages=find_packages(exclude=('tests',)),
    install_requires=[],
)
