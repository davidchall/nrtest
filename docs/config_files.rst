===================
Configuration Files
===================

Metadata about the system under test and each test is stored in JSON configuration files.



Software under test
-------------------

Mandatory fields
~~~~~~~~~~~~~~~~

**name** *[string]*
    Name of the software.
**version** *[string]*
    Version of the software.
**exe** *[string]*
    The executable name. This can also be a path.


Optional fields
~~~~~~~~~~~~~~~

**description** *[string]*
    A short description to help identification of this version.
**setup_script** *[string]*
    Path to a bash script that shall be sourced in order to create the environment needed to run the software.
**timeout** *[float]*
    The period in time [seconds] after which a test will be terminated and considered failed.



Test
----

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
    A list of expected output files. The key is a path to the output file, relative to the directory in which the test is run. The value identifies the file type and determines how it shall be compared to a benchmark.
**fail_strings** *[list of strings]*
    If any of these strings are found in the stdout or stderr streams, the test is considered failed.
