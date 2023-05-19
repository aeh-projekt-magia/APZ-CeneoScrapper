#!/bin/bash
ulimit -n 100000
for xx in 1200
do
    trap "echo Exited!; exit;" SIGINT SIGTERM
    filename_var="locust_reports/report$(date "+%Y%M%d_%H%M%S").html"
    locust \
    --host http://192.168.1.107:5001 \
    --users $xx \
    --spawn-rate 2.5 \
    --autostart \
    --headless \
    --html $filename_var \
    --run-time 10m
done