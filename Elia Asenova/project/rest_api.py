import requests, sys, json
from flask import Flask, jsonify, request
from ensembl_client import EnsemblClient
from exon_processor import ExonProcessor
from sequence_operations import swapNucleotides, processGCContent
from validator import Validator

app = Flask(__name__)
client = EnsemblClient()
validator = Validator()

@app.route('/v1/sequence/gene/id/<id>')
def getGeneInfo(id):
    result = {}
    
    response = client.getRequest("/sequence/id/" + id, { "Content-Type" : "text/plain"})
    if "error" in response.text:
        return json.loads(response.text)
    elif validator.validateObjectType(client, id):
        return validator.validateObjectType(client, id)
    result["seq"] = response.text

    gc_content = request.args.get('gc_content')
    swap = request.args.get('swap')
    content_type = request.args.get('content_type')
    if gc_content or swap:
        return getGCContentSwapSequence(response.text, gc_content, swap)
    if content_type:
        return getSequenceInSpecificFormat(id, response.text, content_type)

    # get exons
    response = client.getRequestWithParams("/lookup/id/" + id, { "Content-Type" : "application/json"}, {"expand" : 1}).json()
    exons = []
    exonsIds = {}
    if "error" not in response:
        for t in response["Transcript"]:
            for e in t["Exon"]:
                if e["id"] not in exonsIds:
                    exon = {}
                    exon["start"] = e["start"]
                    exon["end"] = e["end"]
                    exon["id"] = e["id"]

                    exons.append(exon)
                    exonsIds[e["id"]] = e["id"]
    else:
        return response

    processor = ExonProcessor(len(exons))
    exons = processor.processExons(exons)

    result["exons"] = exons
    return jsonify(result)

def getGCContentSwapSequence(seq, gc_content, swap):
    result = {}
    result["seq"] = seq

    if gc_content and gc_content != "false":
        gc_content_validation = validator.validateGCContentParameter(gc_content)
        if gc_content_validation:
            return gc_content_validation

        result["gc_content"] = processGCContent(seq)

    if swap:
        swap_validation = validator.validateSwapParameter(swap)
        if swap_validation:
            return swap_validation

        swap = swap.split(':')
        result["swap_sequence"] = swapNucleotides(seq, swap[0], swap[1])

    return result

def getSequenceInSpecificFormat(id, seq, content_type):
    result = {}

    content_type_validation = validator.validateContentType(content_type)
    if content_type_validation:
        return content_type_validation

    result["seq"] = seq 
    response = client.getRequest("/lookup/id/" + id, { "Content-Type" : "application/json"}).json()

    if content_type == "fasta":
            result["id"] = ">" + id + '.' + str(response["version"]) + response["description"]
    elif content_type == "multi-fasta":
        result["id"] = ">" + id + '.' + str(response["version"]) + response["description"]

        lookup_response = client.getRequestWithParams("/lookup/id/" + id, { "Content-Type" : "application/json"}, {"expand" : 1}).json()
        exons = []
        exonsIds = {}
        if "error" not in lookup_response:
            for t in lookup_response["Transcript"]:
                for e in t["Exon"]:
                    if e["id"] not in exonsIds:
                        exon = {}
                        exon["id"] = ">" + e["id"]

                        exons.append(exon)
                        exonsIds[e["id"]] = e["id"]
        else:
            return lookup_response

        processor = ExonProcessor(len(exons))
        exons = processor.processExons(exons)
        result["exons"] = exons
    elif content_type == "x-fasta":
        chromosome = "chromosome:" + response["assembly_name"] + ":" + response["seq_region_name"] + ":" + str(response["start"]) + ":" + str(response["end"]) + ":" + str(response["strand"])
        result["id"] = ">" + id + '.' + str(response["version"]) + " " + chromosome + response["description"]

    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)