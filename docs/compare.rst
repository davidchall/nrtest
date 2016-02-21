.. _compare:

Result comparison
-----------------

Currently, the following output file types are supported:

**{default, text}**
    This is equivalent to the ``diff`` command-line utility
**{null, none}**
    No comparison is performed (used when a difference should not indicate a test failure).
**topas binned**
    Compares output of TOPAS binned scorers.
**topas ntuple**
    Compares output of TOPAS ntuple scorers.

I am aware that this list is very limited. In a future version, it will be possible to add custom comparisons via user extensions.
