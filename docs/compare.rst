.. _compare:

Result comparison
-----------------

The routine used to compare a result file to its respective benchmark is determined by its file type. This is specified in the ``output_files`` field of the test, e.g. ``"output_files": {"image.jpg": "default"}``.

Currently, the following output file types are bundled with nrtest:

**default**
    This is equivalent to the ``diff`` command-line utility
**null**
    No comparison is performed (used when a difference should not indicate a test failure).

If there are other comparison routines that are widely applicable I would be very happy to bundle these with nrtest too.

For more specialized comparisons, it is also possible to add custom comparison routines via extensions.



.. _compare_extensions:

Custom comparison routines
~~~~~~~~~~~~~~~~~~~~~~~~~~

An example of how to add custom comparison routines can be found in the `nrtest-topas <https://github.com/davidchall/nrtest-topas>`_ repository. This is a good resource when writing your own extensions.

Comparison functions must be written in Python and must have the following signature:

.. code-block:: python

    def xxx_compare(path_test, path_ref, rtol, atol):

        if compatible:
            return True
        else:
            return False

where ``path_test`` and ``path_ref`` are the paths to the results files produced by the software under test and the reference version, respectively.
The relative tolerance ``rtol`` and the absolute tolerance ``atol`` are set at the command-line (see :ref:`usage`), and should follow these interpretations in order to remain consistent with other comparisons.

In order to register the custom comparison function with nrtest, we pass `entry_points to setuptools <https://pythonhosted.org/setuptools/setuptools.html#dynamic-discovery-of-services-and-plugins>`_ in our setup.py file.
The syntax is

.. code-block:: python

    entry_points = {
        'nrtest.compare': [
            '<file type>=<module.path>:<function_name>'
        ]
    }

where ``<file type>`` is the string that will be used in the configuration file to signify the use of this comparison function, ``<module.path>`` is the dotted module path where the comparison function is found, and ``<function_name>`` is ``xxx_compare`` in this case. More details can be found `here <https://pythonhosted.org/setuptools/setuptools.html#dynamic-discovery-of-services-and-plugins>`_.

