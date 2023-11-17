#!/bin/bash

#runing sflow-rt

#Creating sflow-agents and sending the topology to collector.
#python ./sflowMonitor.py > wypad

#Getting information from sflowtool and calculate the link utilization.
python ./LinkUtilization.py
