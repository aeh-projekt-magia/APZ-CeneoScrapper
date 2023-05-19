#!/bin/bash
ulimit -n 100000
for xx in 2400
do
    trap "echo Exited!; exit;" SIGINT SIGTERM
    filename_var="locust_reports/report$(date "+%Y%M%d_%H%M%S").html"
    locust \
    --host http://192.168.1.107:80 \
    --users $xx \
    --spawn-rate 10 \
    --autostart \
    --headless \
    --html $filename_var \
    --run-time 5m
done