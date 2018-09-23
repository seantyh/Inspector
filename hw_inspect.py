import pyMetrics
import os
import glob
import re
import logging
import ast
from collections import Counter, OrderedDict
from code_data import CodeData
from os.path import join

logger = logging.getLogger("hw_inspect")
logger.setLevel("INFO")

def inspect_homework(hwpath):
    if not os.path.exists(hwpath):
        logger.error("Directory Not Found")
        return 
    
    hw_inspection = OrderedDict()
    id_pat = re.compile(r"_([a-zA-Z][0-9ab]+|es_[0-9]+)_(.*?)_(\d+)")
    for hw_file in glob.glob(join(hwpath, "*.py")):        
        id_mat = id_pat.search(hw_file)
        if not id_mat:
            logger.warning("invalid id: %s", hw_file)
            continue
        
        student_id = id_mat.groups()[0]         

        fin = open(hw_file, "r", encoding="UTF-8")
        codes = fin.read()
        fin.close()
        try:
            tree = ast.parse(codes)
            cdata = CodeData()
            cdata.syntax = "valid"
            cdata.n_char = len(codes)
            cdata.adv_nodes = pyMetrics.get_advance_nodes(tree)
            cdata.imp_modules = pyMetrics.get_import_modules(tree)
            func_list = pyMetrics.get_called_func_names(tree)
            cdata.func_freq = Counter(func_list)
            cdata.str_content = pyMetrics.get_string(tree)            
            cdata.node_vec = pyMetrics.to_type_vec(tree)
            cdata.tree_depth = pyMetrics.tree_depth(tree)
            cdata.n_nodes = pyMetrics.node_count(tree)

            hw_inspection[student_id] = cdata
        except SyntaxError:
            cdata.syntax = "error"
            logger.error("Syntax Error in %s", student_id)

    return hw_inspection    
        