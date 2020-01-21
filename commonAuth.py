# Copied from /opt/splunk/share/splunk/authScriptSamples/commonAuth.py

import getopt
import sys

# read the inputs coming in and put them in a dict for processing.
def readInputs():
    optlist, _ = getopt.getopt(sys.stdin.readlines(), '', ['username=', 'password='])

    returnDict = {}
    for name, value in optlist:
        returnDict[name[2:]] = value.strip()

    return returnDict
