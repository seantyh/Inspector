import numpy as np
from datetime import datetime
from collections import Counter

def summarize_hw_object(hw_object):
    nchar_list = [cdata.n_char for cdata in hw_object.values()]
    nnode_list = [cdata.n_nodes for cdata in hw_object.values()]
    depth_list = [cdata.tree_depth for cdata in hw_object.values()]
    vec_diff_list = [cdata.vec_manhattan for cdata in hw_object.values()]

    func_freq = Counter()
    def_names_freq = Counter()
    imp_modules_freq = Counter()
    for cdata in hw_object.values():
        func_freq.update(cdata.func_freq)
        def_names_freq.update(cdata.def_names)
        imp_modules_freq.update(cdata.imp_modules)

    percentiles = [5,10,25,50,75,90,95]
    stat_data = {
        "timestamp": datetime.now().strftime("%y/%m/%d %H:%M:%S"),
        "length": len(hw_object),
        "n_char": np.percentile(nchar_list, percentiles).tolist(),
        "n_node": np.percentile(nnode_list, percentiles).tolist(),
        "depth": np.percentile(depth_list, percentiles).tolist(),
        "vec_diff": np.percentile(vec_diff_list, percentiles).tolist(),
        "func_call": func_freq,
        "def_names": def_names_freq,
        "imp_modules": imp_modules_freq
    }

    return stat_data

def tag_hw_object(hw_object, hw_stat):

    distinct_func_calls = set()
    distinct_imp_modules = set()
    n_obs = hw_stat["length"]
    for func_x, func_freq in hw_stat["func_call"].items():
        if func_freq < n_obs:
            distinct_func_calls.add(func_x)

    for mod_x, mod_freq in hw_stat["imp_modules"].items():
        if mod_freq < n_obs:
            distinct_imp_modules.add(mod_x)

    for cdata in hw_object.values():
        if cdata.syntax == "error":
            cdata.tags = []
            continue
        tags = []
        # tag by nchar percentiles
        nchar_tag = tag_by_percentiles(cdata.n_char, hw_stat["n_char"])
        nchar_tag = ["n_char_" + x for x in nchar_tag]

        # tag by vec_diff percentiles
        vec_diff_tag = tag_by_percentiles(
                        cdata.vec_manhattan, hw_stat["vec_diff"])
        vec_diff_tag = ["vec_diff_" + x for x in vec_diff_tag]

        # tag by depth percentiles
        depth_tag = tag_by_percentiles(cdata.tree_depth, hw_stat["depth"])
        depth_tag = ["depth_" + x for x in depth_tag]
        tags = nchar_tag + vec_diff_tag + depth_tag

        # tag by less frequent call, modules
        has_distinct_call = any([(x in distinct_func_calls) \
                            for x in cdata.func_freq.keys()])
        has_distinct_mod = any([(x in distinct_imp_modules) \
                            for x in cdata.imp_modules])
        if has_distinct_call:
            tags.append("distinct_call")
        if has_distinct_mod:
            tags.append("distinct_mod")

        cdata.tags = tags
    return hw_object

def tag_by_percentiles(value_x, perct_7, tail="double"):
    # perct_7 :: [Q05, Q10, Q25, Q50, Q75, Q90, Q95]
    tags = []

    if value_x < perct_7[0] and tail != "right":
        tags.append("Q05")
    if value_x < perct_7[1] and tail != "right":
        tags.append("Q10")
    if value_x > perct_7[5] and tail != "left":
        tags.append("Q90")
    if value_x > perct_7[6] and tail != "left":
        tags.append("Q95")
    return tags
