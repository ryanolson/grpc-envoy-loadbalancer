FROM envoyproxy/envoy:latest

RUN apt-get update && apt-get -q install -y --no-install-recommends \
    curl python3-pip

RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install --upgrade setuptools && \
    python3 -m pip install PyYAML

WORKDIR /source/democontroller
COPY . .

#CMD /usr/local/bin/envoy -c /etc/lb.yaml --service-node load-balancer --service-cluster load-balancer
CMD ["/source/democontroller/start_service.sh"]
