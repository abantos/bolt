import os
import sys
print os.getcwd()


def run():
    params = " ".join(sys.argv[1:])
    print "Running with: " + params
