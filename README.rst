===============================
nrtest
===============================

|pypi| |ci| |readthedocs|

``nrtest`` is an end-to-end regression testing framework, designed for scientific software that perform numerical calculations.


Features
--------

``nrtest`` aims to simplify your workflow:

- JSON files describe the software under test and the tests themselves
- result files are stored in a portable benchmark directory
- benchmarks are compared by iterating through tests and their results
- custom comparisons can easily be added through extensions



.. |pypi| image:: https://img.shields.io/pypi/v/nrtest.svg
        :target: https://pypi.python.org/pypi/nrtest
        :alt: PyPI Package

.. |ci| image:: https://github.com/davidchall/nrtest/workflows/CI/badge.svg
        :target: https://github.com/davidchall/nrtest/actions
        :alt: Build Status

.. |readthedocs| image:: https://readthedocs.org/projects/nrtest/badge/?version=latest
        :target: https://nrtest.readthedocs.org/en/latest/?badge=latest
        :alt: Documentation Status
