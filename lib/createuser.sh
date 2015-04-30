#!/bin/bash
user="$1"
opts="$2"

if ! getent passwd ${user} >/dev/null 2>&1
then
    adduser --system ${opts} ${user}
    addgroup --system ${user}
    adduser ${user} ${user}
    echo "added user ${user}"
else
    echo "user ${user} already exists"
fi
