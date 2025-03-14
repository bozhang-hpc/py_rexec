import argparse
from rexec.client_api import remote_func
from rexec.remote_obj import DSDataObj

import dxspaces
import numpy

@remote_func
def hello_world():
    print("hello world!")

@remote_func
def add(a, b):
    return a+b

@remote_func
def ds_add(dsa, dsb):
    return dsa+dsb

@remote_func
def ds_add3(dsa):
    return dsa*2+DSDataObj("arr1", 0, (0,0), (15, 15))*3

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "broker_addr", type=str,
        help="The broker's address to connect."
    )

    parser.add_argument(
        "--broker_port", type=str, default="5559",
        help="The broker's port to connect. [0-65535]"
    )

    parser.add_argument(
        "--dspaces_addr", type=str,
        help="The DataSpaces server addr to connect."
    )

    args = parser.parse_args()

    remote_func().set_remote_addr(args.broker_addr)
    remote_func().set_remote_port(args.broker_port)

    if(args.dspaces_addr):
        dspaces_client = dxspaces.DXSpacesClient(args.dspaces_addr)
        print("Connected to DataSpaces API.")
        arr1 = numpy.ones((16,16))
        dspaces_client.PutNDArray(arr1, "arr1", 0, (0,0))
        dspaces_client.PutNDArray(arr1, "arr2", 0, (0,0))
        print("Put... Done!")

        var1 = DSDataObj("arr1", 0, (0,0), (15, 15))
        var2 = DSDataObj("arr2", 0, (0,0), (15, 15))

        ret = ds_add(var1, var2)
        print(ret)

        ret = ds_add3(var1)
        print(ret)

    ret = hello_world()
    print(ret)

    ret = add(5,2)
    print(ret)

    ret = add(18,33)
    print(ret)