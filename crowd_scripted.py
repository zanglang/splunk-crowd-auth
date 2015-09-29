#!/usr/bin/env python

# This is a Splunk scripted auth implementation that delegates
# the users and group lookups to an Atlassian Crowd server.

import crowd
import json
import os, sys, getpass

from commonAuth import *

with open('/opt/splunk/etc/system/local/crowd.json') as data_file:
    data = json.load(data_file)


app_url = data['server_url']
app_user = data['user']
app_pass = data['password']

splunk_user_group = 'splunk-users'

# Create the reusable Crowd object
cs = crowd.CrowdServer(app_url, app_user, app_pass)

def userLogin( args ):
    success = cs.auth_user(args[USERNAME], args['password'])
    if success:
        print SUCCESS
    else:
        print FAILED

def getUserInfo( args ):
    un = args[USERNAME]
    groups = cs.get_nested_groups(un)
    if groups:
        print SUCCESS + ' --userInfo=' + un + ';' + un + ';' + un + ';' + ':'.join(groups)
    else:
        print FAILED

def getUsers( args ):
    users = cs.get_nested_group_users(splunk_user_group)
    out = SUCCESS
    for un in users:
        groups = cs.get_nested_groups(un)
        out += ' --userInfo=' + un + ';' + un + ';' + un + ';' + ':'.join(groups)

    print out

def getSearchFilter( args ):
    # Ignore search filters
    if cs.user_exists(args[USERNAME]):
        print SUCCESS
    else:
        print FAILED

def main():
    callName = sys.argv[1]
    dictIn = readInputs()

    returnDict = {}
    if callName == "userLogin":
        userLogin( dictIn )
    elif callName == "getUsers":
        getUsers( dictIn )
    elif callName == "getUserInfo":
        getUserInfo( dictIn )
    elif callName == "getSearchFilter":
        getSearchFilter( dictIn )
    else:
        print "ERROR unknown function call: " + callName

if __name__ == "__main__":
    main()
