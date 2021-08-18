from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

setup(
    name='nrtest',
    version='0.2.5',
    description='Numerical regression testing',
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/x-rst',
    author='David Hall',
    author_email='dhcrawley@gmail.com',
    url='https://github.com/davidchall/nrtest',
    license='MIT',
    packages=['nrtest'],
    python_requires='>=3.6.1',
    install_requires=[
        'pydantic',
    ],
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Testing',
        'Natural Language :: English',
    ],
)
