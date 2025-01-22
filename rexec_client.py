import dill as pickle
import sys
import zmq

def hello_world():
    print("hello world!")

def add(a, b):
    return a+b

if __name__ == "__main__":
    fn_ser = pickle.dumps(hello_world)
    print(sys.getsizeof(fn_ser))
    pickle.loads(fn_ser)()

    number = pickle.dumps(1)

    mp_msg = [number, fn_ser]

    zmq_context = zmq.Context()
    zmq_socket = zmq_context.socket(zmq.REQ)
    zmq_socket.connect("tcp://localhost:5559")

    zmq_socket.send_multipart(mp_msg)
    zmq_msg = zmq_socket.recv()
    print(f"Received reply [ {zmq_msg} ]")

    fn_add_ser = pickle.dumps(add)
    add_args = [1, 2]
    add_args_ser = pickle.dumps(add_args)

    number = pickle.dumps(2)
    mp_msg = [number, fn_add_ser, add_args_ser]
    zmq_socket.send_multipart(mp_msg)
    zmq_msg = zmq_socket.recv()
    result = pickle.loads(zmq_msg)
    print(f"Received remote add result [ {result} ]")


    zmq_socket.disconnect("tcp://localhost:5559")
    zmq_socket.close()
    zmq_context.destroy()