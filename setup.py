from setuptools import setup, find_packages

setup(
    name='warehouse-sdk',
    version='0.1.0',
    author='Evgeny Vakhteev',
    author_email='evgeny@dex.guru',
    packages=find_packages(),
    url='https://github.com/dex-guru/warehouse-sdk',
    license='LICENSE.txt',
    description='An SDK for interacting with a Guru Warehouse service.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        "requests>=2.25.1",
        "pydantic>=1.8.2"
        # Add other dependencies needed for your package
    ],
)
