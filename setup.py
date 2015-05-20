from setuptools import setup, find_packages
from distutils.util import convert_path

# Get version from package
ver_path = convert_path('nrtest/__version__.py')
ns = {}
with open(ver_path) as f:
    exec(f.read(), ns)
version = ns['__version__']


setup(
    name='nrtest',
    version=version,
    packages=find_packages(exclude=['testing']),
    scripts=['scripts/nrtest'],

    # dependencies
    install_requires=[
        'six',
        'psutil>=2.0',
        'numpy>=1.6.0',
    ],

    # metadata for upload to PyPI
    author='David Hall',
    description='Numerical regression testing',
    license='MIT',
    url='https://github.com/davidchall/nrtest',
)
