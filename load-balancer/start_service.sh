#!/bin/bash
cd /source/democontroller
./update.sh
cd /source/democontroller
/usr/local/bin/envoy -c /etc/lb.yaml --service-node load-balancer --service-cluster load-balancer
