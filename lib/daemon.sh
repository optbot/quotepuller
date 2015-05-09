#!/bin/bash
TEMP=$(getopt -n "$0" -o a:s:u:v: --long action:,service:,user:,venv: -- "$@")
if [ $? != 0 ] ; then echo "Terminating..." >&2 ; exit 1 ; fi
eval set -- "$TEMP"
while true;
do
    case "$1" in
        -a|--action)
            action="$2"
            shift 2;;
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

PYTHON="${venv}/bin/python"
PIDFILE="/var/run/${user}.pid"
DAEMON_MGR="start-stop-daemon"
INFO_LEVEL="--verbose"

# Cf. https://github.com/mongodb/mongo/blob/47f76710961fb5be17d92e26fb7452f8223afb9f/debian/init.d#L122
# http://stackoverflow.com/questions/16855541/how-to-properly-use-log-daemon-msg-log-end-msg-log-progress-msg-to-write-a-pro
# https://bugs.launchpad.net/ubuntu/+source/lsb/+bug/282638
. /lib/lsb/init-functions

STARTTIME=1

running_pid() {
    pid=$1
    name=$2
    [ -z "$pid" ] && return 1
    [ ! -d /proc/$pid ] &&  return 1
    cmd=`cat /proc/$pid/cmdline | tr "\000" "\n"|head -n 1 |cut -d : -f 1`
    [ "$cmd" != "$name" ] &&  return 1
    return 0
}

running() {
    [ ! -f "$PIDFILE" ] && return 1
    pid=`cat $PIDFILE`
    running_pid $pid $PYTHON || return 1
    return 0
}

start_server() {
    $DAEMON_MGR --background --start $INFO_LEVEL --pidfile $PIDFILE \
        --make-pidfile --chuid $user:$user \
        --exec $PYTHON $service
    errcode=$?
    return $errcode
}

stop_server() {
    $DAEMON_MGR --stop $INFO_LEVEL --pidfile $PIDFILE \
        --retry 300 \
        --user $user \
        --exec $PYTHON
    errcode=$?
    return $errcode
}

case "$action" in
    start)
        log_daemon_msg "Starting ${service}"
        if running
        then
            # log_progress_msg gets overridden in Ubuntu 14.04
            echo "apparently already running"
            log_end_msg 0
            exit 0
        fi
        if start_server
        then
            [ -n "$STARTTIME" ] && sleep $STARTTIME # Wait some time
            if  running ;  then
                log_end_msg 0
            else
                echo "process died after starting"
                log_end_msg 1
            fi
        else
            echo "process could not be started"
            log_end_msg 1
        fi
        ;;
    stop)
        log_daemon_msg "Stopping ${service}"
        if running
        then
            errcode=0
            stop_server || errcode=$?
            log_end_msg $errcode
        else
            echo "apparently not running"
            log_end_msg 0
            exit 0
        fi
        ;;
    *)
        echo "Invalid action: ${action}"
        exit 1
        ;;
esac

exit 0
