#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_process
----------------------------------

Tests for process management.
"""

# system imports
import unittest
import os
from subprocess import check_output
from tempfile import NamedTemporaryFile

# project imports
from nrtest.process import source, execute, monitor


class TestProcess(unittest.TestCase):

    def test_source(self):
        var_name, var_value = 'TESTVAR', 'This is a test'
        with NamedTemporaryFile('w', delete=False) as f:
            f.write('export %s="%s"' % (var_name, var_value))
            script_name = f.name

        env = source(script_name)
        cmd = ['/bin/bash', '-c', 'echo $%s' % var_name]
        stdout = check_output(cmd, env=env, universal_newlines=True)

        os.remove(script_name)
        self.assertEqual(stdout.strip(), var_value)

    def test_duration(self):
        time = 2
        p = execute('sleep %s' % time)
        (_, perf) = monitor(p)
        duration = perf['duration']

        self.assertAlmostEqual(duration, time, delta=1.0)

    def test_timeout(self):
        p = execute('sleep 5')
        (_, perf) = monitor(p, timeout=2)
        duration = perf['duration']

        self.assertIsNone(duration)


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
