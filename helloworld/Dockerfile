FROM grpc/python
COPY --from=envoyproxy/envoy /usr/local/bin/envoy /usr/local/bin/envoy

WORKDIR /source/greeter
COPY . .

ENTRYPOINT ["/source/greeter/start_service.sh"]

