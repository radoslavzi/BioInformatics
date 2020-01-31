import re
from flask import jsonify

class Validator():
    def __init__(self):
        self.errorMsg = {}

    def validateObjectType(self, client, id):
        response = client.getRequest("/lookup/id/" + id, { "Content-Type" : "application/json"}).json()
        if response["object_type"] != "Gene":
            self.errorMsg["error"] = "The id is an id of " + response["object_type"] + ". It should be a Gene id."
            return jsonify(self.errorMsg)

    def validateGCContentParameter(self, gc_content):
        if gc_content != "true":
            self.errorMsg["error"] = "The parameter gc_content is not valid. Allowed values: true or false."
            return jsonify(self.errorMsg)

    def validateSwapParameter(self, swap):
        pattern = re.compile("^[ATGC]{1}:[ATGC]{1}$")
        if not re.search(pattern, swap):
            self.errorMsg["error"] = "The parameter swap should be in the following format N:N."
            return jsonify(self.errorMsg)

    def validateContentType(self, content_type):
        if not content_type == "fasta" and not content_type == "multi-fasta" and not content_type == "x-fasta":
            self.errorMsg["error"] = "The parameter content_type is not valid. Allowed values: fasta, multi-fasta or x-fasta."
            return jsonify(self.errorMsg)
