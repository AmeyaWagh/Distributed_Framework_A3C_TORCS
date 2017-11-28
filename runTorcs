#!/bin/sh

# python3 torcsGame.py
# pkill torcs

# A POSIX variable
OPTIND=1         # Reset in case getopts has been used previously in the shell.
# ./
# Initialize our own variables:
config_file="./torcs_central/config.json"
verbose=0
stopflag=0
# refreshRate = 5 #minutes

usage="$(basename "$0")

Distributed RL framework for Torcs

usage ./runTorcs [Arguments]

Arguments:
    -h              show this help text
    -s              server only
    -c              worker only
    -n              erase models and start new session
    -e config       edit config file

Default:
    -   Both server and client would run on the same computer
        Make sure ip address in config is 'localhost'.
    -   If hosting a server use -s argument.
    -   If running only worker use -c argument. 
        Make sure the server IP is set correctly in config
    -   The trained weights are stored locally as well as on server.
        Use -n argument to start a new worker and server on both systems
        or on the same machine.    
"

while getopts "h?cnse:" opt; do
    case "$opt" in
    h|\?)
        echo "$usage"
        exit 0
        ;;
    c)  python3 torcsGame.py
        pkill torcs
        exit 0
        ;;
    n)  rm -rf models/ pulledModels/ resource/ temp/
        ;;
    s)  ./runServer
        exit 0
        ;;
    e)  nano "$config_file"
        exit 0
        ;;     
    esac
done

shift $((OPTIND-1))

[ "$1" = "--" ] && shift

# echo " Leftovers: $@"

killallprocess(){
    echo "-----------------killing all processes------------------------"
    stopflag=1
    kill -INT $TASK_PID
    pkill torcs
    kill -INT $SERVER_PID
    pkill python3
    exit 0
}
trap killallprocess INT

# running Torcs for long time causes memory leak or lags. kill the worker and start again
runWorker(){
while true;do
    echo "-----------------------------------starting worker-----------------------------------"
    python3 torcsGame.py &
    TASK_PID=$!
    echo " WORKER_PID $TASK_PID"
    sleep 5m
    kill -INT $TASK_PID
    pkill torcs
    if [ "$stopflag" -ne 0 ]; then
        break
    fi
done;   
}


./runServer &
SERVER_PID=$!
echo "SERVER_PID $SERVER_PID"
sleep 10
runWorker
# pkill python3
echo "KILLED WORKER"
exit 0