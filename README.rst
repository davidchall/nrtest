===============================
nrtest
===============================

|pypi| |travis-ci| |coveralls| |readthedocs|

``nrtest`` is an end-to-end regression testing framework, designed for scientific software that perform numerical calculations.


Features
--------

``nrtest`` aims to simplify your workflow:

- JSON files describe the software under test and the tests themselves
- result files are stored in a portable benchmark directory
- benchmarks are compared by iterating through tests and their results
- custom comparisons can easily be added through extensions


.. _basic_usage:

Basic Usage
-----------

As an example usage, we consider testing TOPAS_. This is a Monte Carlo tool for particle simulation, designed for medical physics research. Of course, such a tool must be rigorously validated against experimental data. But it is also useful to frequently run shorter tests, checking for regressions by comparing results to a previous version.

First, we describe the software under test in a configuration file called ``apps/topas-2.0.3.json``. Note that ``setup_script`` defines the environment needed to run the software.

.. code-block:: json

    {
        "name": "topas",
        "version" : "2.0.3",
        "setup_script" : "/path/to/topas-2.0.3/setup.sh",
        "exe" : "topas"
    }

We then describe the test in second configuration file called ``tests/Scoring_01.json``. In doing so, we define the command-line arguments presented to the executable and the input files needed for the test to run. Finally, we also specify the expected output files, and declare how they should be compared to a benchmark. Here we use ``topas binned``, which is a custom comparison routine, though some comparison routines are bundled with nrtest. It is also easy to add your own.

.. code-block:: json

    {
        "name": "Scoring_01",
        "version": "1.0",
        "description": "Basic test shooting a 6cm diameter proton beam into a water phantom.",
        "args": [
            "Scoring_01.txt"
        ],
        "input_files": [
            "Scoring_01.txt",
            "GlobalParameters.txt"
        ],
        "output_files": {
            "Dose.csv": "topas binned"
        }
    }

To execute the test, we tell ``nrtest`` where to find the configuration files and where to output the benchmark. Note that ``nrtest`` will search ``tests/`` for tests, though we could have specified ``tests/Scoring_01.json``.

.. code-block:: bash

    $ nrtest execute apps/topas-2.0.3.json tests/ -o benchmarks/2.0.3
    INFO: Found 1 tests
    Scoring_01: pass
    INFO: Finished

To compare to a previous benchmark:

.. code-block:: bash

    $ nrtest compare benchmarks/2.0.3 benchmarks/2.0.2
    Scoring_01: pass
    INFO: Finished


More advanced usage is detailed in the documentation_.




.. _TOPAS: http://www.topasmc.org
.. _documentation: https://nrtest.readthedocs.org/en/latest


.. |pypi| image:: https://img.shields.io/pypi/v/nrtest.svg
        :target: https://pypi.python.org/pypi/nrtest
        :alt: PyPI Package

.. |travis-ci| image:: https://img.shields.io/travis/davidchall/nrtest.svg
        :target: https://travis-ci.org/davidchall/nrtest
        :alt: Build Status

.. |coveralls| image:: https://coveralls.io/repos/github/davidchall/nrtest/badge.svg?branch=master
        :target: https://coveralls.io/github/davidchall/nrtest?branch=master
        :alt: Code Coverage

.. |readthedocs| image:: https://readthedocs.org/projects/nrtest/badge/?version=latest
        :target: https://nrtest.readthedocs.org/en/latest/?badge=latest
        :alt: Documentation Status
