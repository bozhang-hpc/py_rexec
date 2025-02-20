from client_api.rexec import remote_exec

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