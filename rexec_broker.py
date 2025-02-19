import argparse
import zmq

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--client_port", type=str, default="5559",
        help="The port for listening the clients' requests. [0-65535]"
    )

    parser.add_argument(
        "--server_port", type=str, default="5560",
        help="The port for listening the servers' requests. [0-65535]"
    )

    parser.add_argument(
        "--control_port", type=str, default="5561",
        help="The port for listening the termination signal. [0-65535]"
    )

    args = parser.parse_args()

    context = zmq.Context()

    frontend_addr = "tcp://*:" + args.client_port
    frontend = context.socket(zmq.ROUTER)
    frontend.bind(frontend_addr)

    backend_addr = "tcp://*:" + args.server_port
    backend = context.socket(zmq.DEALER)
    backend.bind(backend_addr)

    control_addr = "tcp://*:" + args.control_port
    control = context.socket(zmq.REP)
    control.bind(control_addr)
    # control.setsockopt_string(zmq.SUBSCRIBE, "")

    try:
        zmq.proxy_steerable(frontend, backend, None, control)
    except KeyboardInterrupt:
        print("W: interrupt received, stopping broker...")
    finally:
        frontend.close()
        backend.close()
        control.close()
        context.term()

if __name__ == "__main__":
    main()
