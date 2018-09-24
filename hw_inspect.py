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

def inspect_homework(hwpath, ref_file=None):
    if not os.path.exists(hwpath):
        logger.error("Directory Not Found")
        return 
    
    if os.path.exists(ref_file):
        fin = open(ref_file, "r", encoding="UTF-8")
        ref_codes = fin.read()
        fin.close()
        ref_tree = ast.parse(ref_codes)
        ref_vec = pyMetrics.to_type_vec(ref_tree)
    else:
        ref_vec = None

    hw_inspection = OrderedDict()
    id_pat = re.compile(r"_([a-zA-Z][0-9ab]+|es_[0-9]+)_(.*?)_(\d+)")
    hw_serial = {}
    hw_file_list = glob.glob(join(hwpath, "*.py"))
    hw_file_list.sort()
    for hw_file in hw_file_list:           
        id_mat = id_pat.search(hw_file)
        if not id_mat:
            logger.warning("invalid id: %s", hw_file)
            continue        
        
        try:
            student_id = id_mat.groups()[0]
            serial = int(id_mat.groups()[2])
            if hw_serial.get(student_id, 0) < serial:
                hw_serial[student_id] = serial
            else:
                logger.info("Already have %s of serial %d, ignore %d",
                    student_id, hw_serial[student_id], serial)
                continue
        except Exception as ex:
            logger.error(ex)
            continue

              

        fin = open(hw_file, "r", encoding="UTF-8")
        codes = fin.read()
        fin.close()
        cdata = CodeData()
        try:
            tree = ast.parse(codes)            
            cdata.syntax = "valid"
            cdata.n_char = len(codes)
            cdata.adv_nodes = pyMetrics.get_advance_nodes(tree)
            cdata.imp_modules = pyMetrics.get_import_modules(tree)
            func_list = pyMetrics.get_called_func_names(tree)
            cdata.func_freq = Counter(func_list)
            cdata.def_names = pyMetrics.get_definition_names(tree)
            cdata.str_content = pyMetrics.get_string(tree)            
            cdata.node_vec = pyMetrics.to_type_vec(tree)
            cdata.tree_depth = pyMetrics.tree_depth(tree)
            cdata.n_nodes = pyMetrics.node_count(tree)            
            if ref_vec:
                cdata.vec_manhattan = pyMetrics.manhattan_distance(
                                        cdata.node_vec, ref_vec)

        except SyntaxError as ex:
            cdata.syntax = "error"
            logger.error(ex)
            logger.error("Syntax Error in %s", student_id)
        hw_inspection[student_id] = cdata

    return hw_inspection    
        
