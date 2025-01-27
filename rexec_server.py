import time
import zmq
import dill as pickle

def fn_recv_exec(zmq_socket):
    while(True):
        zmq_msg = zmq_socket.recv_multipart()
        fn = pickle.loads(zmq_msg[0])

        args = pickle.loads(zmq_msg[1])

        try:
            ret = fn(*args)
        except:
            ret = "Exception Happens!"

        pret = pickle.dumps(ret)

        zmq_socket.send(pret)


if __name__ == "__main__":

    zmq_context = zmq.Context()
    zmq_socket = zmq_context.socket(zmq.REP)
    zmq_socket.connect("tcp://localhost:5560")

    try:
        fn_recv_exec(zmq_socket)
    except KeyboardInterrupt:
        print("W: interrupt received, stopping rexec server...")
    finally:
        zmq_socket.disconnect("tcp://localhost:5560")
        zmq_socket.close()
        zmq_context.destroy()

    # zmq_socket.send_string("World")
    # server.stop()

    # zmq_msg = zmq_socket.recv_multipart()
    # number = pickle.loads(zmq_msg[0])
    # print(f"Received request: {number}")
    # fn_ser = zmq_msg[1]
    # fn_args_ser = zmq_msg[2]
    # fn_args = pickle.loads(fn_args_ser)
    # print(fn_args)
    # result = pickle.loads(fn_ser)(*fn_args)
    # print(result)
    # result_ser = pickle.dumps(result)

    # zmq_socket.send(result_ser)

    