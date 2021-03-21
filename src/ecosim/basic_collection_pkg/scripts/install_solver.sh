#!/bin/bash

apt-get update -y &&  apt-get install -y python-glpk
apt-get update -y &&  apt-get install -y glpk-utils

apt-get update && apt-get install -y python3-pip

pip3 install pyomo

pip3 install grpcio && pip3 install grpcio-tools

pip3 install pandas

pip3 install numpy