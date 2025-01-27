import dill as pickle
import sys
import zmq

def remote_exec(fn):
    def remote_fn(*args):
        pfn = pickle.dumps(fn)
        pargs = pickle.dumps(args)

        zmq_context = zmq.Context()
        zmq_socket = zmq_context.socket(zmq.REQ)
        zmq_socket.connect("tcp://localhost:5559")

        zmq_mp_msg = [pfn, pargs]
        zmq_socket.send_multipart(zmq_mp_msg)

        zmq_ret_msg = zmq_socket.recv()
        ret_msg = pickle.loads(zmq_ret_msg)

        zmq_socket.disconnect("tcp://localhost:5559")
        zmq_socket.close()
        zmq_context.destroy()

        return ret_msg
    return remote_fn

@remote_exec
def hello_world():
    print("hello world!")

@remote_exec
def add(a, b):
    return a+b

if __name__ == "__main__":
    ret = hello_world()
    print(ret)

    ret = add(1,2)
    print(ret)