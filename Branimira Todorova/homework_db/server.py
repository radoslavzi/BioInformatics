import http.client
import sys
import xmltodict
import json
import redis
import os, requests
from collections import Counter
from pymongo import MongoClient 
from flask import Flask, session, request, send_file
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', "secret-key")
conn = http.client.HTTPConnection("ncbi.nlm.nih.gov")

server = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
client = MongoClient("mongodb://localhost:27017")
db = client.test
redis_host = "localhost"
redis_port = 6379
redis_password = ""
my_redis = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
 
@app.route('/searchByCriteria/<query>')
def searchByCriteria(query):

    cached = my_redis.get(query)
    if(cached):
        return cached
    else:    
        in_db = db.pubmed.find_one({"query" : query})
        if(in_db):
            my_redis.set(query, in_db["res"])
            return in_db["res"]
        else:    
            json_data = getFromPubmed("esearch.fcgi?db=pubmed&term=", query)
            db.pubmed.insert_one({ "query" : query, "res" : json_data})
            my_redis.set(query, in_db["res"])   
            return json_data

def getFromPubmed(url, query):
    r = requests.get(server + url + query)
    my_dict=xmltodict.parse(r.content)
    json_data=json.dumps(my_dict)
 
    return json_data

@app.route('/searchById/<id>')
def searchById(id):

    cached = my_redis.get(id)
    if(cached):
        return cached
    else:    
        in_db = db.pubmed.find_one({"id" : id})
        if(in_db):
            my_redis.set(id, in_db["res"])
            return in_db["res"]
        else:    
            json_data = getFromPubmed("esummary.fcgi?db=pubmed&id=", id)
            db.pubmed.insert_one({ "id" : id, "res" : json_data})
            my_redis.set(id, in_db["res"])   
            return json_data
           
    return json_data

if __name__ == '__main__':

	app.run(host='localhost', port=5000, debug=False)    