import numpy as np
from datetime import datetime
from collections import Counter

def summarize_hw_object(hw_object):
    nchar_list = [cdata.n_char for cdata in hw_object.values()]
    nnode_list = [cdata.n_nodes for cdata in hw_object.values()]
    vec_diff_list = [cdata.vec_manhattan for cdata in hw_object.values()]

    func_freq = Counter()
    def_names_freq = Counter()
    for cdata in hw_object.values():
        func_freq.update(cdata.func_freq)
        def_names_freq.update(cdata.def_names)
        
    percentiles = [5,10,25,50,75,90,95]
    stat_data = {
        "timestamp": datetime.now().strftime("%y/%m/%d %H:%M:%S"),
        "length": len(hw_object),
        "n_char": np.percentile(nchar_list, percentiles).tolist(),
        "n_node": np.percentile(nnode_list, percentiles).tolist(),
        "vec_diff": np.percentile(vec_diff_list, percentiles).tolist(),
        "func_call_freq": func_freq,
        "def_names": def_names_freq
    }

    return stat_data