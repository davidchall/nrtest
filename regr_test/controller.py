from regr_test import run
import os.path


def perform_test(app, test):

    # Catch pre-test errors
    for fname in [app.setup_script, app.exe] + test.in_files:
        if not os.path.isfile(fname):
            return '%s does not exist' % fname

    if not os.path.isdir(test.cwd):
        return '%s does not exist' % test.cwd

    cmd = ' '.join([app.exe] + test.args)
    timeout = None

    # Catch live errors
    try:
        env = run.source(app.setup_script)
        log_file = open(test.log_file, 'w')
        proc = run.execute(cmd, env=env, cwd=test.cwd, stdout=log_file)
        (exit_code, duration, performance) = run.monitor(proc, timeout=timeout)
    except IOError:
        return 'Unable to write log file: "%s"' % test.log_file
    finally:
        log_file.close()

    # Catch post-test errors
    if exit_code == -11:
        return 'Segmentation fault'
    elif exit_code != 0:
        return 'Non-zero exit code'

    if duration is None:
        return 'Program timed out (duration > %ss)' % timeout

    if len(test.fail_strings) > 0:
        with open(test.log_file) as f:
            for line in f:
                if any(s in line for s in test.fail_strings):
                    return 'Failure string found in log file'

    for fname in test.out_files:
        if not os.path.isfile(fname):
            return 'Output file not generated: "%s"' % fname

    # TODO: check log file for failure strings
    # TODO: do something with duration and performance data
