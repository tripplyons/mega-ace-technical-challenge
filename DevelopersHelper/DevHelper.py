import json
import hashlib

def GenerateTEAL(filename : str):
    with open(filename, 'r') as f:
        obj = json.load(f)



    return ""  #should return your generated TEAL code