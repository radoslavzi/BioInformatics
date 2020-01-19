import http.client
import sys
import json
import os, requests
from collections import Counter
from flask import Flask, session, request, send_file
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', "secret-key")
conn = http.client.HTTPConnection("rest.ensembl.org")

server = "https://rest.ensembl.org"

def getExons(exonsDecoded, offset):

    if not offset:
        offset = 0
    else:
        offset = int(offset) * 10
    ids = []
    current = 0
    info = {}
    for item in exonsDecoded["Transcript"]:
        for i in item["Exon"]:
            current +=1
            if(offset <= current and offset + 10 >= current):
                info[i["id"]] = { "start" : i["start"], "end" : i["end"]}
                ids.append(str(i["id"]))

    res = []
    if(len(ids) > 0):
        postQuery = "/sequence/id?content-type=application/json"
        resPost = requests.post(server+postQuery, data=json.dumps({ "ids" : ids}), headers={ "Content-Type" : "application/json"})

        exonSeq = json.loads(resPost.text)
        for ex in exonSeq:
            ex["end"] = info[ex["id"]]["end"]
            ex["start"] = info[ex["id"]]["start"]
            res.append(ex)

    return res

@app.route('/v1/sequence/gene/id/<id>')
def sequence(id):
    
    ext = "/sequence/id/" + id 
    
    r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
    decoded = r.json()

    result = { "seq" : decoded["seq"], "exons" : []}
    extExon = "/lookup/id/" + id + "?expand=1"
    res = requests.get(server+extExon, headers={ "Content-Type" : "application/json"})
    exonsDecoded = res.json()

    offset = request.args.get('offset')
    result["exons"] = getExons(exonsDecoded, offset)
   
    swap = request.args.get('swap')
    if(swap):
        sequence = decoded["seq"]
        t = ''.maketrans(swap[0]+swap[2],swap[2]+swap[0])
        sequence = sequence.translate(t)
        result["swap"] = sequence

    gcContent = request.args.get('gc_content')
    if(gcContent and json.loads(gcContent.lower())):
        res = Counter(decoded["seq"])
        result["gc_content"] = res['G'] + res['C']

    response = app.response_class(
        response=json.dumps(result),
        status=200,
        mimetype='application/json'
    )

    return response

@app.route('/v1/sequence/id/<id>')
def sequence_swap(id):

    ext = "/sequence/id/" + id 
    r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
    decoded = r.json()

    contentType = request.args.get('content-type')
    if( not contentType):
        contentType = "fasta"

    desc = ">" + decoded["id"] + "." + str(decoded["version"]) + " " + decoded["desc"]
    if(contentType == "fasta" or contentType == "multi-fasta"):
        result = desc + "\n" + decoded["seq"]
    elif(contentType == 'x-fasta'):
        result = { "id" : desc, "seq" : decoded["seq"]}    
           
    return result



if __name__ == '__main__':
	app.run(host='localhost', port=5000, debug=False)    

