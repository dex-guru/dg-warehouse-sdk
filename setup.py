from setuptools import setup, find_packages

setup(
    name='DexGuru Warehouse SDK',
    version='0.1',
    packages=find_packages(exclude=['tests*']),
    license='MIT License',
    description='SDK for warehouse queries',
    long_description=open('README.md').read(),
    install_requires=["pydantic", "requests"],
    url='https://github.com/dex-guru/dg-warehouse-sdk',
    author='DexGuru'
)
