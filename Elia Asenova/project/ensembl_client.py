import requests, sys, json

class EnsemblClient:
    def __init__(self):
        self.server = "http://rest.ensembl.org"

    def getRequest(self, endpoint, headers):
        response = requests.get(self.server+endpoint, headers=headers)

        return response

    def getRequestWithParams(self, endpoint, headers, params):
        response = requests.get(self.server+endpoint, headers=headers, params=params)

        return response