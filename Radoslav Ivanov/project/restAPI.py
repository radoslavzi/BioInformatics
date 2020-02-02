import requests, sys
from flask import Flask, session, request, send_file

app = Flask(__name__)

SERVER = "https://rest.ensembl.org"
GENE_ID_EXT = '/sequence/id/'
EXON_EXT = '/lookup/id/'

@app.route('/v1/sequence/gene/id/<id>')
def gene(id):
    sequence = requests.get(SERVER + GENE_ID_EXT + id, headers={ "Content-Type" : "application/json"}).json()['seq']
    exons = requests.get(SERVER + EXON_EXT + id + '?expand=1', headers={ "Content-Type" : "application/json"}).json()
    responseExons =  buildExonResponse(exons['Transcript'], str(sequence))
    gcContent = request.args.get('gc_content')
    swap =  request.args.get('swap')
    contentType = request.args.get('content-type')

    if gcContent:
        calculateGCContent(swap, seq)
    else:
        return  {'seq': sequence, 'exons': responseExons}

def calculateGCContent(swap, seq):
    replaceDict = {}
    if swap:
        replaceDict = dict({swap[0]: swap[2]})
    
    return {'seq': seq,
        'gc_content': seq.count('G') + seq.count('Ç'),
        'swap_sequence': replace(seq, replaceDict)
    }

def buildExonResponse(transcripts, sequence):
    result = list()

    for trans in transcripts:
        for exon in trans['Exon']:
            result.append(
                {'start': exon['start'], 
                'end': exon['end'],
                'id': exon['id'],
                'seq': sequence[exon['start']:exon['end']]
                })

    return result
   
def replace(sequence, replaceDict):
        generatedSeq = ''

        for ch in sequence:
            val = replaceDict.get(ch)
            if(not(val is None)):
                generatedSeq += replaceDict.get(ch)
            else:
                generatedSeq += ch

        return generatedSeq

app.run()