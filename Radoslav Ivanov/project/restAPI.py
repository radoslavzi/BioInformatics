import requests, sys
from flask import Flask, request

app = Flask(__name__)
SERVER = "https://rest.ensembl.org"
GENE_ID_EXT = '/sequence/id/'
EXON_EXT = '/lookup/id/'

@app.route('/v1/sequence/gene/id/<id>')
def gene(id):
    sequence = requests.get(SERVER + GENE_ID_EXT + id, headers={ "Content-Type" : "application/json"}).json()
    exons = requests.get(SERVER + EXON_EXT + id + '?expand=1', headers={ "Content-Type" : "application/json"}).json()
    
    gcContent = request.args.get('gc_content')
    swap =  request.args.get('swap')
    contentType = request.args.get('content-type')

    if gcContent:
        return calculateGCContent(swap, sequence['seq'])
    elif contentType:
        return getSequenceByContentType(id, sequence, contentType)
    else:
        responseExons =  buildExonResponse(exons.get('Transcript'), str(sequence['seq']))
        return  {'seq': sequence, 'exons': responseExons}

def getSequenceByContentType(id, sequence, contentType):

    if contentType == 'fasta':
        return fasta(id, sequence)
    elif contentType == 'x-fasta':
        return xFasta(id, sequence)
    else:
        return multiFasta(id, sequence)

def fasta(id, sequence):
    desc = ">" + sequence["id"] + "." + str(sequence["version"]) + " " + sequence["desc"]
    return desc + "\n" + sequence["seq"]

def xFasta(id, sequence):
    desc = ">" + sequence["id"]
    return desc + "\n" + sequence["seq"]

def multiFasta(id, sequence):
    result = ''
    for seq in sequence:
        desc = ">" + sequence["id"] + "." + str(sequence["version"]) + " " + sequence["desc"]
        result += desc + "\n" + seq["seq"]
    
    return result

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

    if not(transcripts):
        return ''

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