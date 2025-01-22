import zmq

def main():
    context = zmq.Context()

    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5561")

    socket.send_string("TERMINATE")

    socket.close()
    context.destroy()

if __name__ == "__main__":
    main()