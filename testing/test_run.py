from regr_test import run

from subprocess import check_output
import os


def test_source():
    script = 'test_env.sh'
    var_name, var_value = 'TESTVAR', 'This is a test'
    with open(script, 'w') as f:
        f.write('export %s="%s"' % (var_name, var_value))

    env = run.source(script)
    cmd = ['/bin/bash', '-c', 'echo $%s' % var_name]
    stdout = check_output(cmd, env=env, universal_newlines=True)

    os.remove(script)
    assert stdout.strip() == var_value


def test_duration():
    time = 2
    p = run.execute('sleep %s' % time)
    (duration, data) = run.monitor(p)

    assert abs(duration-time) < 1.0


def test_timeout():
    p = run.execute('sleep 5')
    (duration, data) = run.monitor(p, timeout=2)

    assert duration is None
