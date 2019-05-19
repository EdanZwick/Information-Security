import os
import subprocess
import sys

import infosec.utils


TEST_COMMAND = 'echo "I am g`whoami`!"; exit'
COMMAND_RESULT = 'I am groot!'


def error(message):
    print('\x1b[31m{}\x1b[0m'.format(message))


def check_q1():
    with infosec.utils.in_directory('q1'):
        result = infosec.utils.execute([sys.executable, 'q1.py', TEST_COMMAND])
        if COMMAND_RESULT not in result.stdout:
            error('ERROR: Failed running a root command with `python q1.py <CMD>`')
            return False
        return True


def check_q2a():
    with infosec.utils.in_directory('q2'):
        if os.path.isfile('core'):
            os.remove('core')
        result = infosec.utils.execute([sys.executable, 'q2a.py'])
        if not os.path.exists('core'):
            error('ERROR: Running q2a.py did not generate a `core` file')
            return False
        return True


def check_q2b():
    with infosec.utils.in_directory('q2'):
        result = infosec.utils.execute([sys.executable, 'q2b.py'], TEST_COMMAND)
        if COMMAND_RESULT not in result.stdout:
            error('ERROR: Failed running a root command shell with `python q2b.py`')
            return False
        return True


def check_if_nonempty(path):
    if not os.path.exists(path):
        error('ERROR: {} does not exist'.format(path))
        return False
    with open(path) as reader:
        data = reader.read().strip()
    if not data:
        error('ERROR: {} is empty'.format(path))
        return False
    return True


def smoketest():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    if all([
        check_q1(),
        check_q2a(),
        check_q2b(),
        check_if_nonempty('q1/q1.txt'),
        check_if_nonempty('q2/q2a.txt'),
        check_if_nonempty('q2/q2b.txt'),
        check_if_nonempty('q2/shellcode.asm'),
    ]):
        print('smoketest seems cool')


if __name__ == '__main__':
    smoketest()
