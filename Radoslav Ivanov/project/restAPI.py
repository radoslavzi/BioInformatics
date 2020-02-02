from flask import Flask
import requests, sys
from sample_exam import SequenceBuilder

app = Flask(__name__)
SERVER = "https://rest.ensembl.org"
GENE_ID_EXT = '/sequence/id/'
#ENSG00000157764
EXON_EXT = '/lookup/id/'

class EnsembleAPI:

    def __init__(self, seq):
        self.seq = seq

    @app.route('/v1/sequence/gene/id/<id>')
    def gene(self, id):
       # sequence = requests.get(SERVER + GENE_ID_EXT + id, headers={ "Content-Type" : "application/json"}).json()
       # exons = requests.get(SERVER + EXON_EXT + id + '?expand=1', headers={ "Content-Type" : "application/json"}).json()
        #responseExons =  self.buildExonResponse(exons['Exon'], '')
        return 'dsa'
    
    def buildExonResponse(self, exons, sequence):
        result = list()

        for exon in exons:
            result.append(
                {'start': exon['start'], 
                'end': exon['end'],
                'id': exon['id'],
                'seq': sequence[exon['start']:exon['end']]
                })

        return result

    def run(self):
        app.run(debug=True)

EnsembleAPI('seq').run()