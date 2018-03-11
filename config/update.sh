#!/bin/bash
docker exec -ti grpcenvoyloadbalancer_load-balancer_1 ./update.sh
#if [ -e new.yaml ]; then
#  mv -f new.yaml eds.yaml
#fi
