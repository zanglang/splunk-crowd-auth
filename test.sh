#!/bin/bash
set -e

USERNAME="test_user"
PASSWORD="password"
SCRIPT="./crowd_scripted.py"

OUT=$(echo -ne "--username=${USERNAME}\n--password=${PASSWORD}" | 2>/dev/null ${SCRIPT} userLogin)
if [[ $OUT != --status=success* ]]; then
    echo "Expected --status=success, got: $OUT"
    exit 1
fi

OUT=$(echo -ne "--username=${USERNAME}\n--password=zz${PASSWORD}" | 2>/dev/null ${SCRIPT} userLogin)
if [[ $OUT != --status=fail* ]]; then
    echo "Expected --status=fail, got: $OUT"
    exit 1
fi

OUT=$(echo -ne "--username=${USERNAME}" | 2>/dev/null ${SCRIPT} getUserInfo)
if [[ $OUT != --status=success* ]]; then
    echo "Expected --status=success, got: $OUT"
    exit 1
fi

OUT=$(echo -ne "--username=does_not_exist" | 2>/dev/null ${SCRIPT} getUserInfo)
if [[ $OUT != --status=fail* ]]; then
    echo "Expected --status=fail, got: $OUT"
    exit 1
fi

OUT=$(echo -ne "--username=${USERNAME}" | 2>/dev/null ${SCRIPT} getSearchFilter)
if [[ $OUT != --status=success* ]]; then
    echo "Expected --status=success, got: $OUT"
    exit 1
fi

OUT=$(echo -ne "--username=does_not_exist" | 2>/dev/null ${SCRIPT} getSearchFilter)
if [[ $OUT != --status=fail* ]]; then
    echo "Expected --status=fail, got: $OUT"
    exit 1
fi

OUT=$(echo -ne "" | 2>/dev/null ${SCRIPT} getUsers)
if [[ $OUT != --status=success* && $OUT == *jenkins_check_user* ]]; then
    echo "Expected --status=success, got: $OUT"
    exit 1
fi

echo "All passed."