import argparse
from client_api.rexec import remote_exec

@remote_exec
def hello_world():
    print("hello world!")

@remote_exec
def add(a, b):
    return a+b

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

    args = parser.parse_args()

    remote_exec().set_remote_addr(args.broker_addr)
    remote_exec().set_remote_port(args.broker_port)

    ret = hello_world()
    print(ret)

    ret = add(1,2)
    print(ret)

    ret = add(18,33)
    print(ret)