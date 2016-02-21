.. _config_test:

Configuration: test
-------------------

Metadata about each test is stored in a JSON configuration file. See :ref:`basic_usage` for an example of the syntax.

The following fields can be used to describe a single test.



Mandatory fields
~~~~~~~~~~~~~~~~

**name** *[string]*
    Name of the test.
**version** *[string]*
    Version of the test.
**args** *[list of strings]*
    A list of command-line arguments that will be passed to the software under test.



Optional fields
~~~~~~~~~~~~~~~

**description** *[string]*
    A short description to help identification of this version.
**input_files** *[list of strings]*
    A list of required input files. Each path is specified relative to the location of the configuration file itself.
**output_files** *[dict of string-string pairs]*
    A list of expected output files. The key is a path to the output file, relative to the working directory when the test is run. The value identifies the file type, which determines how it shall be compared to a benchmark (see :ref:`compare`).
**fail_strings** *[list of strings]*
    If any of these strings are found in the stdout or stderr streams, the test is considered failed.
