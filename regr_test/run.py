import six
import os

import subprocess
import psutil
# Using psutil.Process.wait() in unconventional manner
from psutil import TimeoutExpired as ProcessNotFinished

from datetime import datetime
from collections import namedtuple


def source(script, old_env=None):
    """Emulates source in bash and returns the resulting environment object.
    """
    script = os.path.abspath(script)
    if not os.path.isfile(script):
        return None

    # Force use of bash shell
    cmd = ['/bin/bash', '-c', 'source %s; env' % script]
    stdout = subprocess.check_output(cmd, env=old_env, universal_newlines=True)

    return dict((line.split('=', 1) for line in stdout.splitlines()))


def execute(cmd, stdin=None, stdout=None, stderr=subprocess.STDOUT,
            cwd=None, env=None):
    """Execute command as child process.

    Args:
        cmd: either a string containing the entire command to be executed, or
        a sequence of program arguments.
        Other arguments are the usual subprocess.Popen() arguments.

    Returns:
        Instance of the psutil.Popen class. This provides the methods of the
        subprocess.Popen and psutil.Process classes in a single interface.
    """
    # Tokenize string into arguments
    if isinstance(cmd, six.string_types):
        import shlex
        cmd = shlex.split(cmd)

    # Don't pass kwargs because I want to limit functionality
    return psutil.Popen(cmd, stdin=stdin, stdout=stdout, stderr=stderr,
                        cwd=cwd, env=env)


def monitor(proc, timeout=None, min_dt=1, max_ndata=10):
    """Monitor the status of a process and record performance data. If the
    number of measurements exceeds max_ndata, the data is resampled and the
    time between measurements is increased.

    Args:
        proc:      instance of psutil.Popen class.
        timeout:   time after which process will be killed [seconds].
        min_dt:    minimum time between performance measurements [seconds].
        max_ndata: maximum number of performace measurements.

    Returns:
        (exit_code, duration, data) where data is a list of performance
        measurements. Duration is set to None if the process times out.
    """
    resampling_factor = 2

    time_init = datetime.fromtimestamp(proc.create_time())
    dt = min_dt
    ndata = 0
    data = []

    # This block uses the psutil.Process.wait() method in an unconventional
    # manner, in order to precisely determine the process duration, whilst
    # also choosing the sampling rate of performance measurements. Please only
    # edit if you fully understand how this works, as it is easy to break.
    while True:
        try:
            exit_code = proc.wait(dt)

            # Process has finished
            duration = (datetime.now() - time_init).total_seconds()
            break

        # Process has not finished
        except ProcessNotFinished:

            t = (datetime.now() - time_init).total_seconds()

            # Measure performance
            try:
                data.append(_measure_performance(proc, t))
                ndata += 1
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                continue

            # Kill process if it passes user-selected timeout
            if timeout and t >= timeout:
                proc.kill()
                exit_code = 0
                duration = None
                break

            # Resample data if necessary
            if ndata >= max_ndata:
                del data[::resampling_factor]
                ndata = len(data)
                dt *= resampling_factor

    return (exit_code, duration, data)


def _measure_performance(proc, time):
    """Measure performance statistics of process.

    Args:
        proc: instance of psutil.Popen class.
        time: time at which measurement is made (is appended to data).

    Returns:
        namedtuple containing a data point.
    """
    cpu_usage = proc.cpu_percent()
    mem_usage = float(proc.memory_info().rss) / 1024 / 1024  # MB

    # TODO: IO counters not available on OS X, but could use on Linux
    # read_usage = float(proc.io_counters().read_bytes) / 1024 / 1024  # MB
    # write_usage = float(proc.io_counters().write_bytes) / 1024 / 1024  # MB

    Performance = namedtuple('Performance', 'time, cpu_usage, mem_usage')
    return Performance(time, cpu_usage, mem_usage)
