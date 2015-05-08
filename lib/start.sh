#!/bin/bash
DAEMON=/usr/bin/python

TEMP=$(getopt -n "$0" -o s:u:v: --long service:,user:,venv: -- "$@")
if [ $? != 0 ] ; then echo "Terminating..." >&2 ; exit 1 ; fi
eval set -- "$TEMP"
while true;
do
    case "$1" in
        -s|--service)
            service="$2"
            shift 2;;
        -u|--user)
            user="$2"
            shift 2;;
        -v|--venv)
            venv="$2"
            shift 2;;
        --)
            shift
            break;;
    esac
done

echo "service: ${service}"
echo "user: ${user}"
echo "venv: ${venv}"
echo "DAEMON: ${DAEMON}"
