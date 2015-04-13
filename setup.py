from setuptools import setup, find_packages

setup(
    name='regr-test',
    version='0.0.1',
    packages=find_packages(exclude=['testing']),

    # dependencies
    install_requires=[
        'six',
        'psutil>=2.0'
    ],

    # metadata for upload to PyPI
    author='David Hall',
    description='Numerical regression testing',
    license='MIT',
    url='https://github.com/davidchall/regr-test',
)
