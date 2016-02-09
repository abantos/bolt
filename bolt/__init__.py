import os
import sys
print os.getcwd()

print "There is something to create a conflict"

def run():
    params = " ".join(sys.argv[1:])
    print "Running with: " + params
