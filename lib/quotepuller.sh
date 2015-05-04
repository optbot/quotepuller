#!/bin/bash
user=$(id -un)
group=$(id -gn)
TEMP=$(getopt -n "$0" -o d:l:s:v: --long dbconn:,logs:,serv:,venvs: -- "$@")
if [ $? != 0 ] ; then echo "Terminating..." >&2 ; exit 1 ; fi
eval set -- "$TEMP"
while true;
do
    case "$1" in
        -d|--dbconn)
            dbconn="$2"
            shift 2;;
        -l|--logs)
            logs="$2"
            shift 2;;
        -s|--serv)
            service="$2"
            shift 2;;
        -v|--venvs)
            venvs="$2"
            shift 2;;
        --)
            shift
            break;;
    esac
done

echo "user: ${user}"
echo "group: ${group}"
echo "venvs: ${venvs}"
echo "logs: ${logs}"
echo "dbconn: ${dbconn}"
echo "service: ${service}"
