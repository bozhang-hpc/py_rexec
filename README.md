# Python Remote Execution
This repository contains the implementation of remote execution capabilities in [SciDx software stack](https://scidx.sci.utah.edu/) with the support to [DataSpaces](https://dataspaces.sci.utah.edu/) Data Staging framework. It provides a simple user interface to python programmer (including jupyter notebook) to execute arbitary user-defined functions on the remote Points-of-Presence (PoPs).

## Requirements
* Python 3.8+
* [PyZMQ](https://pypi.org/project/pyzmq/)
* [dill](https://pypi.org/project/dill/)
* [DXSpaces](https://pypi.org/project/DXSpaces/) (If DataSpaces is needed)

## Usage
### Remote Function Execution
Adding `@remote_func` before function definition.
```python
from rexec.client_api import remote_func

@remote_func
def hello_world():
    print("hello world!")

ret = hello_world()
print(ret) ### None

@remote_func
def add(a, b):
    return a+b

ret = add(5,2)
print(ret) ### 7
```

### Remote Function Execution using External Library
`import` external libraries in the beginning of the remote function implementation.
```python
from rexec.client_api import remote_func

@remote_func
def numpy_max(array):
    ### import the external libraries first
    import numpy as np

    ### Implement function logic
    return np.max(array)
```

### Remote Function Execution on DataSpaces Data Objects
Declare `DSDataObj(name, version, lb, ub)` locally, then use it inside the remote function.
```python
from rexec.client_api import remote_func
from rexec.remote_obj import DSDataObj

@remote_func
def ds_add(dsa, dsb):
    return dsa+dsb

var1 = DSDataObj("arr1", 0, (0,0), (15, 15))
var2 = DSDataObj("arr2", 0, (0,0), (15, 15))

ret = ds_add(var1, var2)
print(ret)
```

## License
This project is licensed under the [MIT License](LICENSE).