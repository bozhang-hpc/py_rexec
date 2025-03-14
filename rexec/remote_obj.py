import logging
import dill
import dxspaces

class DSDataObj:
    ctx = "client"
    dspaces_client = None

    def __new__(cls, name, version, lb, ub, namespace=None):
        if cls.ctx == "server":
            return DSDataObj.resolve(name, version, lb, ub, namespace)
        return super().__new__(cls)
    
    def __init__(self, name, version, lb, ub, namespace=None):
        self.name = name
        self.version = version
        self.lb = lb
        self.ub = ub
        self.data = None

    @staticmethod
    def resolve(name, version, lb, ub, namespace=None):
        #### DSPACES_GET()
        if(DSDataObj.dspaces_client):
            logging.info(f"dspaces_get(): var={name}, version={version}, lb={lb}, ub={ub}, namespace={namespace}")
            return DSDataObj.dspaces_client.GetNDArray(name, version, lb, ub, namespace)

@dill.register(DSDataObj)
def save_DSDataObj(pickler, obj):
    pickler.save_reduce(DSDataObj.resolve, (obj.name, obj.version, obj.lb, obj.ub), obj=obj)
