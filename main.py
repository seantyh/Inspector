import os
import json
import logging
import argparse
from os.path import basename, normpath
from code_data import CodeDataEncoder
from hw_inspect import *
from summarize import summarize_hw_object, tag_hw_object

logging.basicConfig(level="INFO")
def main():    
    parser = argparse.ArgumentParser()
    parser.add_argument("hwpath")
    parser.add_argument("-r", "--ref-file", help='reference file')
    args = parser.parse_args()
    if args.hwpath:        
        hw_object = inspect_homework(args.hwpath, args.ref_file)
        hw_stat = summarize_hw_object(hw_object)
        hw_object = tag_hw_object(hw_object, hw_stat)
        hw_summary = OrderedDict([("stat", hw_stat), ("codes", hw_object)])
        hwid = basename(normpath(args.hwpath))
        if not os.path.exists("data/out"):
            os.makedirs("data/out")
        with open("data/out/inspection_%s.json" % hwid, 
                "w", encoding="UTF-8") as fout:
            json.dump(hw_summary, fout, 
                cls=CodeDataEncoder,
                ensure_ascii=False, indent=2)
    

if __name__ == "__main__":
    main()




