import zmq

def main():
    context = zmq.Context()

    frontend = context.socket(zmq.ROUTER)
    frontend.bind("tcp://*:5559")

    backend = context.socket(zmq.DEALER)
    backend.bind("tcp://*:5560")

    control = context.socket(zmq.REP)
    control.bind("tcp://*:5561")
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
