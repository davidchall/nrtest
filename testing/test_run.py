from nose.tools import assert_almost_equals

from regr_test import run


def test_duration():
    time = 2
    p = run.execute('sleep %s' % time)
    (duration, data) = run.monitor(p)
    assert_almost_equals(duration, time, places=0)


def test_timeout():
    p = run.execute('sleep 5')
    (duration, data) = run.monitor(p, timeout=2)
    assert duration is None
