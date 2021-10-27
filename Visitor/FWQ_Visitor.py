from __future__ import print_function

import logging

import grpc


import sys
sys.path.append('C:/Users/serge/source/repos/SD-FWQ/Registry')
import Registry_pb2
import Registry_pb2_grpc

def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    channel = grpc.insecure_channel('localhost:50051')
    stub = Registry_pb2_grpc.RegistryServiceStub(channel)
    response = stub.Registry(Registry_pb2.RegistryRequest(ID=1,name="you",password="12345"))
    print("Client received: " + response.response)

if __name__ == "__main__":
    logging.basicConfig()
    run()
