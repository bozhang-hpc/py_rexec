import time
import zmq
import dill as pickle

class HelloRPC(object):
    def hello(self, name):
        return "Hello, %s" % name


if __name__ == "__main__":

    zmq_context = zmq.Context()
    zmq_socket = zmq_context.socket(zmq.REP)
    zmq_socket.connect("tcp://localhost:5560")

    zmq_msg = zmq_socket.recv_multipart()
    number = pickle.loads(zmq_msg[0])
    print(f"Received request: {number}")
    fn_ser = zmq_msg[1]
    pickle.loads(fn_ser)()

    time.sleep(1)

    zmq_socket.send_string("World")
    # server.stop()

    zmq_msg = zmq_socket.recv_multipart()
    number = pickle.loads(zmq_msg[0])
    print(f"Received request: {number}")
    fn_ser = zmq_msg[1]
    fn_args_ser = zmq_msg[2]
    fn_args = pickle.loads(fn_args_ser)
    print(fn_args)
    result = pickle.loads(fn_ser)(*fn_args)
    print(result)
    result_ser = pickle.dumps(result)

    zmq_socket.send(result_ser)

    zmq_socket.disconnect("tcp://localhost:5560")
    zmq_socket.close()
    zmq_context.destroy()