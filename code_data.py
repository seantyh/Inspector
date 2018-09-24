import json

class CodeData:
    def __init__(self):
        self.syntax = "NA"
        self.adv_nodes = []
        self.imp_modules = []
        self.node_vec = None
        self.str_content = []
        self.func_freq = {}
        self.def_names = []
        self.n_nodes = 0
        self.tree_depth = 0
        self.n_char = 0
        self.vec_manhattan = -1
        self.tags = []
    
class CodeDataEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, CodeData):
            cdata_map = obj.__dict__
            cdata_map["node_vec"] = "not serialized"
            return cdata_map
        return json.JSONEncoder.default(self, obj)