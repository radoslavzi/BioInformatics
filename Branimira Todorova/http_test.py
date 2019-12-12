import http.client
import sys
import json

conn = http.client.HTTPConnection("rest.ensembl.org")
conn.request("GET", "family/id/PTHR10903_SF46?", headers={"Content-Type": "application/json"})
response = conn.getresponse()
print(response.status)
print(response.reason)

binary_res = response.read().decode()
family = json.loads(binary_res)
#print(family["members"][0:3])

for item in family["members"][0:3]:
    conn.request("GET", "sequence/id/"+item["gene_stable_id"], headers={"Content-Type": "application/json"})
    response = conn.getresponse()
    print(response.read().decode())
    #print(item["gene_stable_id"])