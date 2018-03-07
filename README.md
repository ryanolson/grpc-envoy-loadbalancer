# Envoy + gRPC - Basic Load-Balancing

This example used an edge-proxy (frontend/front-envoy) to accept incoming GRPC calls
and routes them to a set of backend services which fullfil the requests.

The client creates a single gRPC stub to the edge-proxy and calls `stub.SayHelloRequest`
10 times.  When both helloworld services are up and running each succesive call gets
properly load-balanced between the backend services.  This is an example of L7 load-
balancing of HTTP2 requests.

## Quickstart

In one window,
```
docker-compose up
```

In another window, run the client:
```
cd client
docker-compose run --rm client
```

You can target each of the individual instances on ports `9001` and `9002` respectively.

Example output:

```
ubuntu@dgx:~/gtc_18/envoy/examples/grpc-proxy/client$ docker-compose run --rm client
Greeter client received: Hello, you from host=ca2310cf3b73!
Greeter client received: Hello, you from host=114c199e6bdb!
Greeter client received: Hello, you from host=ca2310cf3b73!
Greeter client received: Hello, you from host=114c199e6bdb!
Greeter client received: Hello, you from host=ca2310cf3b73!
Greeter client received: Hello, you from host=114c199e6bdb!
Greeter client received: Hello, you from host=ca2310cf3b73!
Greeter client received: Hello, you from host=114c199e6bdb!
Greeter client received: Hello, you from host=ca2310cf3b73!
Greeter client received: Hello, you from host=114c199e6bdb!
ubuntu@dgx:~/gtc_18/envoy/examples/grpc-proxy/client$ ADDRESS=localhost:9001 docker-compose run --rm client
Greeter client received: Hello, you from host=ca2310cf3b73!
Greeter client received: Hello, you from host=ca2310cf3b73!
Greeter client received: Hello, you from host=ca2310cf3b73!
Greeter client received: Hello, you from host=ca2310cf3b73!
Greeter client received: Hello, you from host=ca2310cf3b73!
Greeter client received: Hello, you from host=ca2310cf3b73!
Greeter client received: Hello, you from host=ca2310cf3b73!
Greeter client received: Hello, you from host=ca2310cf3b73!
Greeter client received: Hello, you from host=ca2310cf3b73!
Greeter client received: Hello, you from host=ca2310cf3b73!
ubuntu@dgx:~/gtc_18/envoy/examples/grpc-proxy/client$ ADDRESS=localhost:9002 docker-compose run --rm client
Greeter client received: Hello, you from host=114c199e6bdb!
Greeter client received: Hello, you from host=114c199e6bdb!
Greeter client received: Hello, you from host=114c199e6bdb!
Greeter client received: Hello, you from host=114c199e6bdb!
Greeter client received: Hello, you from host=114c199e6bdb!
Greeter client received: Hello, you from host=114c199e6bdb!
Greeter client received: Hello, you from host=114c199e6bdb!
Greeter client received: Hello, you from host=114c199e6bdb!
Greeter client received: Hello, you from host=114c199e6bdb!
Greeter client received: Hello, you from host=114c199e6bdb!
```
