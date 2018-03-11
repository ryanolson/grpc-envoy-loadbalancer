# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function
import os
import grpc

import helloworld_pb2
import helloworld_pb2_grpc


def run():
    channel = grpc.insecure_channel(os.environ.get("ADDRESS"))
    for i in range(1000):
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        try:
            response = stub.SayHello(helloworld_pb2.HelloRequest(name='you'))
            if i%200 in [0, 1]:
                print("Greeter client received: " + response.message)
        except:
            if i%100 in [0, 1]:
                print("Greeter client failed")
            pass


if __name__ == '__main__':
    run()
