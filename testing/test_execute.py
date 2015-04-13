from regr_test import execute


def test_sleep():
    cmd = 'sleep 5'
    p = execute.execute_process(cmd)
    (duration, data) = execute.monitor_process(p)
