from nrtest.process import source, execute, monitor

import os
from subprocess import check_output
from tempfile import NamedTemporaryFile


def test_source():
    var_name, var_value = 'TESTVAR', 'This is a test'
    with NamedTemporaryFile('w', delete=False) as f:
        f.write('export %s="%s"' % (var_name, var_value))
        script_name = f.name

    env = source(script_name)
    cmd = ['/bin/bash', '-c', 'echo $%s' % var_name]
    stdout = check_output(cmd, env=env, universal_newlines=True)

    os.remove(script_name)
    assert stdout.strip() == var_value


def test_duration():
    time = 2
    p = execute('sleep %s' % time)
    (_, perf) = monitor(p)
    duration = perf['duration']

    assert abs(duration-time) < 1.0


def test_timeout():
    p = execute('sleep 5')
    (_, perf) = monitor(p, timeout=2)
    duration = perf['duration']

    assert duration is None
