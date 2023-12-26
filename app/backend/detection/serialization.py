import numpy as np
from json import JSONEncoder
import json

class NumpyArrayEncoder(JSONEncoder):
   def default(self, obj):
       if isinstance(obj, np.ndarray):
           return obj.tolist()
       return JSONEncoder.default(self, obj)
   
def serialize_for_numpy(value):
    return json.dumps(value, cls=NumpyArrayEncoder)

def numpy_arrays_to_lists(value):
    return json.loads(serialize_for_numpy(value))