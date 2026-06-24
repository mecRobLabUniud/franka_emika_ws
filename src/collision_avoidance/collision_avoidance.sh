#!/bin/bash

# trap 'kill 0' EXIT INT TERM
# 
# dir="$(dirname $0)"
# skeleton_tracking_dir="$HOME/Desktop/skeleton_tracking"
# 
# start_demo="roslaunch collision_avoidance demo.launch"
# start_main="python3 $dir/scripts/demo_stop_event_traj.py"
# start_calcduration="python3 $dir/scripts/calc_stop_duration_server.py"
# start_flagstop="python3 $dir/scripts/flag_stop_server.py"
# start_vision="bash $skeleton_tracking_dir/exec.sh --stream --gui 19"
# 
# $start_demo &
# sleep 1
# $start_main &
# $start_calcduration &
# $start_flagstop &
# sleep 1
# $start_vision


trap 'kill 0' EXIT INT TERM

dir="$(dirname $0)"
mode=$1
use_gui=$2
test=$3
skeleton_tracking_dir="$HOME/Desktop/skeleton_tracking"

start_demo="roslaunch collision_avoidance demo.launch"
start_main="python3 $dir/scripts/demo_stop_event_traj.py"
start_calcduration="python3 $dir/scripts/calc_stop_duration_server.py"
start_flagstop="python3 $dir/scripts/flag_stop_server.py"

if [ "$mode" == "--track" ]; then
    if [ "$use_gui" == "--gui" ]; then
        start_vision="bash $skeleton_tracking_dir/exec.sh --track --gui"
    else
        start_vision="bash $skeleton_tracking_dir/exec.sh --track"
    fi

elif [ "$mode" == "--stream" ]; then
    if [ -z "$test" ]; then
        echo "No test number provided. Please provide a test number."
        exit 1
    else
        n_test=$test
    fi

    if [ "$use_gui" == "--gui" ]; then
        start_vision="bash $skeleton_tracking_dir/exec.sh --stream --gui $n_test"
    else
        start_vision="bash $skeleton_tracking_dir/exec.sh --stream $n_test"
    fi

fi




$start_demo &
sleep 1
$start_main &
$start_calcduration &
$start_flagstop & 
sleep 1
$start_vision
