from setuptools import setup, find_packages

setup(
    name="metaboscan",
    version="1.0",
    packages=find_packages(),
    package_data={
        'REPORT_METABOSCAN': ['assets/*'],
    },
)