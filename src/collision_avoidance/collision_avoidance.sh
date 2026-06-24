#!/bin/bash

trap 'kill 0' EXIT INT TERM

dir="$(dirname $0)"
skeleton_tracking_dir="$HOME/Desktop/skeleton_tracking"

start_demo="roslaunch collision_avoidance demo.launch"
start_main="python3 $dir/scripts/demo_stop_event_traj.py"
start_calcduration="python3 $dir/scripts/calc_stop_duration_server.py"
start_flagstop="python3 $dir/scripts/flag_stop_server.py"
start_vision="bash $skeleton_tracking_dir/exec.sh --stream --gui"

$start_demo &
sleep 1
$start_main &
$start_calcduration &
$start_flagstop &
sleep 1
$start_vision


