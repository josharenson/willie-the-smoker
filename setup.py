from setuptools import find_packages, setup

setup(
    name='willie-the-smoker',
    version='1.0.0',
    packages=find_packages(),
    scripts=["willie-the-smoker/bin/josh-jam"],
    include_package_data=True,
    zip_safe=False
)
