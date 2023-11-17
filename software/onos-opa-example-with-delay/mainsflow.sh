#!/bin/bash

#runing sflow-rt

#Creating sflow-agents and sending the topology to collector.
python2 ./Sflow-skrypty/sflowMonitor.py 

#Getting information from sflowtool and calculate the link utilization.
python2 ./Sflow-skrypty/LinkUtilization.py
