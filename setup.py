from setuptools import setup, find_packages


setup(
    name='pbac',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'pydantic==1.10.6',
    ],
    python_requires='>=3.11'
)
