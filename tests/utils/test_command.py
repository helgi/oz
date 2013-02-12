#!/usr/bin/python
import sys
import os

try:
    import py.test
except ImportError:
    print('Unable to import py.test.  Is py.test installed?')
    sys.exit(1)

# Find oz
prefix = '.'
for i in range(0,3):
    if os.path.isdir(os.path.join(prefix, 'oz')):
        sys.path.insert(0, prefix)
        break
    else:
        prefix = '../' + prefix

try:
    import oz.utils.Command
except ImportError:
    print('Unable to import oz.  Is oz installed?')
    sys.exit(1)

# test oz.ozutil.executable_exists
def test_exe_exists_bin_true():
    oz.utils.Command.executable_exists('/bin/true')

def test_exe_exists_foo():
    with py.test.raises(Exception):
        oz.utils.Command.executable_exists('foo')

def test_exe_exists_full_foo():
    with py.test.raises(Exception):
        oz.utils.Command.executable_exists('/bin/foo')

def test_exe_exists_not_x():
    with py.test.raises(Exception):
        oz.utils.Command.executable_exists('/etc/hosts')

def test_exe_exists_relative_false():
    oz.utils.Command.executable_exists('false')

def test_exe_exists_none():
    with py.test.raises(Exception):
        oz.utils.Command.executable_exists(None)
