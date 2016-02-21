.. _config_sw:

Configuration: software
-----------------------

Metadata about the system under test is stored in a JSON configuration file. See :ref:`basic_usage` for an example of the syntax.

The following fields can be used to describe the software under test.



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

