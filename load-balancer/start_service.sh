#!/bin/bash
cd /source/democontroller
./controller.py
/usr/local/bin/envoy -c /etc/lb.yaml --service-node load-balancer --service-cluster load-balancer &
./controller.py --daemon
