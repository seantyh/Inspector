import argparse
from hw_inspect import *
import logging
import json
from code_data import CodeDataEncoder
from os.path import basename, normpath

logging.basicConfig(level="INFO")
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("hwpath")

    args = parser.parse_args()
    if args.hwpath:
        hw_object = inspect_homework(args.hwpath)
        hwid = basename(normpath(args.hwpath))
        with open("data/inspection_%s.json" % hwid, 
                "w", encoding="UTF-8") as fout:
            json.dump(hw_object, fout, 
                cls=CodeDataEncoder,
                ensure_ascii=False, indent=2)
    

if __name__ == "__main__":
    main()




