from nose.tools import assert_almost_equals

from regr_test import execute


def test_duration():
    time = 2
    p = execute.execute_process('sleep %s' % time)
    (duration, data) = execute.monitor_process(p)
    assert_almost_equals(duration, time, places=0)


def test_timeout():
    p = execute.execute_process('sleep 5')
    (duration, data) = execute.monitor_process(p, timeout=2)
    assert duration is None
