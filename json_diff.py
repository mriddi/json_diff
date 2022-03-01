from functools import reduce
import json
import os
import argparse
import traceback


def get_value(json, key_path: list):
    try:
        if len(key_path) == 1:
            return json[key_path[0]]
        else:
            return get_value(json[key_path.pop(0)], key_path)
    except Exception:
        print ("Dose not found in a.json, but there is in b.json: ", key_path)
        return -1

def get_jsons_diff_no_ordered(json_1, json_2, key_path: list):  
    kp = key_path
    for key in json_2.keys():
        if type(json_2[key]) == int: # worck if field is num
            if key != "start_line" and json_2[key] != 0: # filter fields to be changed AND check logic: 01->1 else 0
                nkp = kp.copy()
                nkp.append(key)
                val = get_value(json_1, nkp)
                if val > 0: json_2[key] = 0 # change key's value using check logic 
        elif type(json_2[key]) == dict: # reiterate if field is dic
            nkp = kp.copy()
            nkp.append(key)         
            get_jsons_diff_no_ordered(json_1, json_2[key], nkp) # iterate in deeper
        else:
            print ("Unknown behaviour, need deep code check") # should never be called
    return json_2    


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description='Input arguments are reading')
        parser.add_argument("jsons", default=["a.json", "b.json"], nargs='*', type=str)
        parser.add_argument("-r", action="store_true") # reverse file order: file_1, file_2 -> file_2, file_1
        args = parser.parse_args()
        if args.r:
            file_1 = os.path.abspath(args.jsons[1])
            file_2 = os.path.abspath(args.jsons[0])
        else:
            file_1 = os.path.abspath(args.jsons[0])
            file_2 = os.path.abspath(args.jsons[1])
    except Exception:
        print(f"Something went wrong with input arguments reading:\n", traceback.format_exc())
    else:  
        with open(file_1) as json_file_1, open(file_2) as json_file_2:
            json_1 = json.load(json_file_1) 
            json_2 = json.load(json_file_2)
            try:
                json_3 = get_jsons_diff_no_ordered(json_1, json_2, [])
            except Exception:
                print(f"Something went wrong with calculatung diff:\n", traceback.format_exc())
            else:  
                with open("c.json", "w") as json_file_3: 
                    json.dump(json_3, json_file_3)
                    print(f"Job was done") 
