from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import sys

def try_to_parse_num(s):
    try:
        return float(s)
    except ValueError:
        return s

def parse_object(url):
    dic = {}
    with open(url, 'r') as csvfile:
        lines = csvfile.readlines()
        for line in lines[1:]:
            keys = line.split(",")
            for key in keys:
                key_value = key.split(":")
                if len(key_value) == 2:
                    value = try_to_parse_num(key_value[1].rstrip())
                    dic[key_value[0].rstrip()] = value
            yield dic
            dic = {}

if __name__ == '__main__':
    url = str(sys.argv[1])
    type = str(sys.argv[2])
#"mongodb://62.44.127.198:27017"
    client = MongoClient(url)
    db = client.test

    print("Authentication si success")

    index = 0
    if type == "sample":
        iterator = parse_object('test_data/Sample.csv')
        for _object in iterator:
            print("Add new entry in sample index = {}".format(index))
            res = db.samples.insert_one(_object)
            print(res)
        
        exit()
    
    index = 0
    if type == "hugosymbol":
        iterator = parse_object('test_data/HugoSymbol.csv')
        for _object in iterator:
            index = index + 1
            print("Add new entry in hugosymbol index = {}".format(index))
            res = db.hugosymbol.insert_one(_object)
            print(res)

        exit()
 
    for u in db.samples.find({"_id": ObjectId("5ca230af10edba1f5e900e2a")}):
        print(u.keys())
