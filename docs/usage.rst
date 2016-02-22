.. highlight:: shell
.. _usage:

Usage
-----

The package provides an ``nrtest`` script with two subcommands: **execute** and **compare**.



Execute
~~~~~~~

The minimal arguments required to execute a test are::

    $ nrtest execute /path/to/software.json /path/to/test.json

The configuration files for the :ref:`software under test <config_sw>` and the :ref:`test itself <config_test>` are documented elsewhere.

Results files and information about the test outcome are stored within a portable benchmark directory. By default, this is ``benchmarks/new`` but this can be specified::

    $ nrtest execute /path/to/software.json /path/to/test.json -o benchmarks/v2.0

It is also possible to specify a directory containing multiple test configuration files instead of a single test::

    $ nrtest execute /path/to/software.json /path/to/tests



Compare
~~~~~~~

The minimal arguments required to compare the newly created benchmark to a reference benchmark are::

    $ nrtest compare benchmarks/new benchmarks/old

This will iterate through each of the tests contained in the benchmark and then compare each result file to its respective reference file. The type of comparison performed is determined by the output file type specified in the test configuration file (see :ref:`compare`).

Comparisons of numerical result files might compare the difference to a tolerance in order to decide if the results are compatible. Relative and absolute tolerances can be specified::

    $ nrtest compare benchmarks/new benchmarks/old --rtol=0.01 --atol=0.0

These are the default tolerances.
