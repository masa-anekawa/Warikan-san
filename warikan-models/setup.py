from setuptools import setup, find_packages

setup(
   name="warikan-models",
   packages=find_packages(exclude=("tests",)),
   include_package_data=True,
   test_suite='nose.collector',
)