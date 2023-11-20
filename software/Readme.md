## Folder contents:
The delayAnalyzer folder contains a program that in real time calculates the delays occurring in the tested topology. It is launched and used by policy engine.

Inside the onos-opa-example-with-delay directory there are policy engine files. In addition, there are scripts using Sflow software to monitor losses occurring in the tested network topology. They are automatically launched and used by policy engine.

The scripts directory contains a script that launches the onos application (activateonosapps.sh) and several basic test scenarios (python files).


## General requirements:
* python2 >= 2.7
* python3 
* Onos 2.4.0
* sFlow-RT
* sflowtool
* Mininet 2.3.0

## Python3 requirements:
* matplotlib>=1.3.1
* networkx==2.2

## Start-up instructions
Use the following commands to run the project, start onos:
```
$ sudo mn -c
$ bazel run onos-local -- clean
```
After launching onos, in a separate terminal enter:
```
$ ./scripts/activateonosapps.sh
$ sudo python3 pl.py &> pingLogs.txt
```
After creating the topology, in a separate terminal run:
```
$ onos localhost imr:startmon 194 org.onosproject.ifwd
$ python3 onos-opa-example-with-delay/main.py
```