import logging
import argparse
import zmq
import dill

from rexec.remote_obj import DSDataObj

import dxspaces

DSDataObj.ctx = "server"

def fn_recv_exec(zmq_socket):
    while(True):
        zmq_msg = zmq_socket.recv_multipart()
        fn = dill.loads(zmq_msg[0])

        args = dill.loads(zmq_msg[1])

        try:
            ret = fn(*args)
        except Exception as e:
            ret = f"An unexpected error occurred: {e}"

        pret = dill.dumps(ret)

        zmq_socket.send(pret)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "broker_ip", type=str,
        help="The broker's ip address to connect. In [0-255].[0-255].[0-255].[0-255] format."
    )

    parser.add_argument(
        "--broker_port", type=str, default="5560",
        help="The broker's port to connect. [0-65535]"
    )

    parser.add_argument(
        "--dspaces_addr", type=str,
        help="The DataSpaces server addr to connect."
    )

    parser.add_argument(
        "-v", "--verbose",
        help="Be verbose",
        action="store_const", dest="loglevel", const=logging.INFO,
    )

    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)

    zmq_addr = "tcp://" + args.broker_ip + ":" + args.broker_port

    zmq_context = zmq.Context()
    zmq_socket = zmq_context.socket(zmq.REP)
    zmq_socket.connect(zmq_addr)

    dspaces_client = None
    if(args.dspaces_addr):
        dspaces_client = dxspaces.DXSpacesClient(args.dspaces_addr)
        logging.info("Connected to DataSpaces API.")
        DSDataObj.dspaces_client = dspaces_client

    try:
        fn_recv_exec(zmq_socket)
    except KeyboardInterrupt:
        print("W: interrupt received, stopping rexec server...")
    finally:
        zmq_socket.disconnect(zmq_addr)
        zmq_socket.close()
        zmq_context.destroy()