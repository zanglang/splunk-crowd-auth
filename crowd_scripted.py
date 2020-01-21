#!/usr/bin/env python

# This is a Splunk scripted auth implementation that delegates
# the users and group lookups to an Atlassian Crowd server.

from __future__ import print_function
import argparse
import crowd
import json
import os
from commonAuth import readInputs


SCRIPTPATH = os.path.dirname(os.path.abspath(__file__))
USERNAME = "username"
USERTYPE = "role"
SUCCESS = "--status=success"
FAILED = "--status=fail"

#################################################################

with open(os.path.join(SCRIPTPATH, 'crowd.json')) as data_file:
    data = json.load(data_file)

app_url = data['server_url']
app_user = data['app_user']
app_pass = data['app_pass']
allowed_groups = data["allowed_groups"]
allowed_group_prefix = data["allowed_group_prefix"]

# Create the reusable Crowd object
cs = crowd.CrowdServer(app_url, app_user, app_pass)
if not cs.auth_ping():
    raise Exception("Unable to connect to Crowd, please check the credentials.")


def userLogin(args):
    success = cs.auth_user(args[USERNAME], args['password'])
    if success:
        print(SUCCESS)
    else:
        print(FAILED)


def getUserGroups(username):
    groups = cs.get_nested_groups(username)
    if groups:
        for g in sorted(groups):
            if g in allowed_groups:
                yield g
            if g.startswith("splunk_"):
                yield g.replace("splunk_", "")


def getUserInfo(args):
    un = args[USERNAME]
    groups = list(getUserGroups(un))
    if groups:
        print(SUCCESS + " --userInfo=%s;%s;%s;%s" % (un, un, un, ':'.join(groups)))
    else:
        print(FAILED)


def getUsers(_):
    users = [user for group in allowed_groups for user in cs.get_nested_group_users(group)]

    out = SUCCESS
    for un in users:
        groups = getUserGroups(un)
        out += " --userInfo=%s;%s;%s;%s" % (un, un, un, ':'.join(groups))

    print(out)


def getSearchFilter(args):
    # Ignore search filters
    un = args[USERNAME]
    groups = list(getUserGroups(un))
    if groups:
        print(SUCCESS)
    else:
        print(FAILED)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("action", help="Authentication action to perform", choices=(
        "userLogin",
        "getUserInfo",
        "getUsers",
        "getSearchFilter"
    ))
    args = p.parse_args()

    dictIn = readInputs()
    globals()[args.action](dictIn)


if __name__ == "__main__":
    main()
