"""
This is the main module that exposes the required functions to use bolt in your applications.
"""
import os
import sys
print os.getcwd()


def run():
    """
    Entry point for the `bolt` executable.

    :return: 0 if the application succeeds or a non-zero value otherwise.
    """
    params = " ".join(sys.argv[1:])
    print "Running with: " + params
    return 0
