from pymongo import MongoClient 
import os
from neo4j import GraphDatabase, basic_auth

def readFile(inFileName):
    inFile = open(inFileName,'r', buffering=100)
    res = inFile.readlines()
    inFile.close()
    return res

def processNodesMiRNA(neo4jSession): 

    data = readFile("mirna-codes.txt")
    for line in data:
        query = "CREATE (a: MirnaCodes { name: '" + line.strip() + "'})"     
        print(query)    
        neo4jSession.run(query, parameters={})



def processNodesClinical(neo4jSession, mongoDb): 

    i = 0
    for clinicalDocument in mongoDb.clinical.find():
        #print(document)
        if clinicalDocument["Data Type"] == 'miRNA Expression Quantification':
            query = "CREATE (a: Clinical" 
            options = ""
            for key in clinicalDocument.keys():
                    if key == "Case ID":
                        options +=   " name : \'" + clinicalDocument[key]  + "\'," 
       
            query += " { " + options[0:len(options)-1] + "} )"
            
            print(query)     
            neo4jSession.run(query, parameters={})

def processVertex(neo4jSession, mongoDb):

    for clinicalDocument in mongoDb.clinical.find():
        mirna = mongoDb.mirna.find_one({"fileName" : clinicalDocument['File Name']})
        if mirna != None:
            for el in mirna["data"]:
                if int(el["read_count"]) > 100:
                    query = "MATCH (a:Clinical),(b:MirnaCodes)"
                    query += " WHERE a.name = '" + clinicalDocument["Case ID"] + "' AND b.name = '" + el["miRNA_ID"] + "'"
                    query += " CREATE (a)-[r:mutation]->(b)"
                    query += " SET r.read_count='" + el["read_count"] + "'"
                    query += " SET r.reads_per_million='" + el["reads_per_million_miRNA_mapped"] + "'"

                    
                    print(query)
                    neo4jSession.run(query, parameters={})
                else :
                    print("no match")    
                    
                



def main():
    driver = GraphDatabase.driver(
    "bolt://34.224.17.173:35394", 
    auth=basic_auth("neo4j", "jewel-tuesdays-payment"))


    session = driver.session()

    client = MongoClient("mongodb://localhost:27017")
    mongodb = client.test
    #processNodesClinical(session, mongodb)
    #processNodesMiRNA(session)

    #processVertex(session, mongodb)
    session.close()
    client.close()
    

if __name__ == '__main__':
    main()    