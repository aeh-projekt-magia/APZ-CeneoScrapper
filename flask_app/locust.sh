#!/bin/bash
for xx in 1200
do
    trap "echo Exited!; exit;" SIGINT SIGTERM
    filename_var="locust_reports/report$(date "+%Y%M%d_%H%M%S").html"
    locust \
    --host http://127.0.0.1:5000 \
    --users $xx \
    --spawn-rate 2.5 \
    --autostart \
    --html $filename_var \
    --run-time 10m
done