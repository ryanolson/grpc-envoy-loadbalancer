#!/bin/bash
if [ -z ${SERVICE_CLUSTER+x} ]; then
  echo "SERVICE_CLUSTER is not defined in the environment"
else
  cd /source/greeter
  python greeter_server.py &
  envoy -c ./service-envoy.yaml --service-cluster ${SERVICE_CLUSTER}
fi
