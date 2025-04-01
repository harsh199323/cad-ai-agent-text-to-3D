from setuptools import setup, find_packages

setup(
    name='cad_builder',
    version='0.1.0',
    description='Package for building CAD models with given natural language requests',
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['*.*']}
)
