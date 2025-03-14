import argparse
import zmq

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "broker_addr", type=str,
        help="The broker's address to connect."
    )

    parser.add_argument(
        "--broker_port", type=str, default="5561",
        help="The broker's control port to connect. [0-65535]"
    )

    args = parser.parse_args()
    
    context = zmq.Context()

    socket = context.socket(zmq.REQ)

    zmq_addr = "tcp://" + args.broker_addr + ":" + args.broker_port
    socket.connect(zmq_addr)

    socket.send_string("TERMINATE")

    socket.close()
    context.destroy()