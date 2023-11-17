#!/bin/bash
echo "OPENFLOW"
onos-app localhost activate org.onosproject.openflow

echo "FWD"
onos-app localhost activate org.onosproject.imr

echo "ARP"
onos-app localhost activate org.onosproject.proxyarp 

echo "LAYOUT"
onos-app localhost activate org.onosproject.layout

echo "PATH PAINTER"
onos-app localhost activate org.onosproject.pathpainter

echo "IFWD"
onos-app localhost install! /home/mich/emu/onos-app-samples/ifwd/target/onos-app-ifwd-2.4.0-SNAPSHOT.oar

#onos-app localhost activate org.onosproject.ifwd
