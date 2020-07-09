import etcd3
import requests
from flask import Flask
from pymongo import MongoClient
from threading import Thread

app = Flask(__name__)
host = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils'
payload = {'db': 'pubmed', 'retmode': 'json'}
clientMongo = MongoClient('localhost', 27017)
dbMongo = clientMongo.documents
clientEtcd = etcd3.client(port=2380)

@app.route('/v1/document/term/<term>')
def get_documents(term):
    if is_data_in_cache(term):
        return read_data_from_db("terms", term)
    else:
        write_data_to_cache(term)

        payload['term'] = term
        response = requests.get(host + '/esearch.fcgi', params=payload)

        write_data_to_db("terms", response.json(), term)
        return response.json()

@app.route('/v1/document/id/<id>')
def get_specific_document(id):
    if is_data_in_cache(id):
        return read_data_from_db("ids", id)
    else:
        write_data_to_cache(id)

        payload['id'] = id
        response = requests.get(host + '/esummary.fcgi', params=payload)

        write_data_to_db("ids", response.json(), id)
        return response.json()

def is_data_in_cache(criteria):
    if clientEtcd.get(criteria) != (None, None):
        return True
    
    return False

def read_data_from_db(collection, criteria):
    return dbMongo[collection].find_one({"_id" : criteria})

def write_data_to_cache(data):
    clientEtcd.put(data, 'cached')

def write_data_to_db(collection, data, criteria):
    data["_id"] = criteria
    dbMongo[collection].insert_one(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)