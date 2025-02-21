import dill as pickle
import sys
import zmq

class remote_exec:
    broker_addr = None
    broker_port = "5559"

    @classmethod
    def set_remote_addr(cls, addr):
        cls.broker_addr = addr
    
    @classmethod
    def set_remote_port(cls, port):
        cls.broker_port = port

    def __init__(self, func=None):
        if func is not None:
            self.func = func

    def __call__(self, *args):
        pfn = pickle.dumps(self.func)
        pargs = pickle.dumps(args)

        zmq_context = zmq.Context()
        zmq_socket = zmq_context.socket(zmq.REQ)
        zmq_addr = "tcp://" + self.broker_addr + ":" + self.broker_port

        zmq_socket.connect(zmq_addr)

        zmq_mp_msg = [pfn, pargs]
        zmq_socket.send_multipart(zmq_mp_msg)

        zmq_ret_msg = zmq_socket.recv()
        ret_msg = pickle.loads(zmq_ret_msg)

        zmq_socket.disconnect(zmq_addr)
        zmq_socket.close()
        zmq_context.destroy()

        return ret_msg