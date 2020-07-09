import http.client
import sys
import json
import populatedataset
estimator = populatedataset.cluster_k_means()
from bson import json_util
import os, requests
from collections import Counter
from flask import Flask, session, request, send_file
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', "secret-key")
from pymongo import MongoClient 
client = MongoClient("mongodb://localhost:27017")
mongodb = client.test

@app.route('/clinical', methods =['GET', 'POST', 'PUT', 'DELETE'])
def clinicalData():
    req = request.get_json() 
    if request.method == "GET":
        res = mongodb.clinical.find_one({ 'Case ID' : req["case_id"] })
        if(res != None):
            return json.loads(json_util.dumps(res))
        
    elif request.method == "POST":   
        mongodb.clinical.insert(req)

    elif request.method == "PUT":  
        mongodb.clinical.update_one({ 'case_id' : req["case_id"] }, {"$set": req}, upsert=True)

    elif request.method == "DELETE":  
        mongodb.clinical.remove({ 'case_id' : req["case_id"] })
    
    return "ok"


@app.route('/mirna-data', methods =['GET', 'POST', 'PUT', 'DELETE'])
def mirnaData():
    req = request.get_json() 
    if request.method == "GET":
        res = mongodb.mirna.find_one({ 'miRNA_ID' : req["mirna_id"] })
        if(res != None):
            return json.loads(json_util.dumps(res))
        
    elif request.method == "POST":   
        mongodb.mirna.insert(req)

    elif request.method == "PUT":  
        mongodb.mirna.update_one({ 'miRNA_ID' : req["mirna_id"] }, {"$set": req}, upsert=True)

    elif request.method == "DELETE":  
        mongodb.mirna.remove({ 'miRNA_ID' : req["mirna_id"] })
    return "ok"    


@app.route('/profiling', methods =['POST'])
def profiling():
    req = request.get_json() 
   
    res = estimator.predict([req["mirna"]])

    return  str(res)

  

if __name__ == '__main__':
    
	app.run(host='localhost', port=5000, debug=False)    

