"""
This is the main module that exposes the required functions to use bolt in your applications.
"""
import argparse
import os
import sys


from _bterror import InvalidTask


def run():
    """
    Entry point for the `bolt` executable.

    :return: 0 if the application succeeds or a non-zero value otherwise.
    """
    params = " ".join(sys.argv[1:])
    print "Running with: " + params
    return 0


def _get_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('task', nargs='?', default='default')
    parser.add_argument('--bolt-file', default='boltfile.py')
    return parser
