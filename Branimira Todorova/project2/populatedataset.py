from pymongo import MongoClient 
import os
from neo4j import GraphDatabase, basic_auth
from sklearn.datasets import load_files
from sklearn import datasets
from sklearn.utils import Bunch
import numpy as np
import csv

def readFile(inFileName):
    inFile = open(inFileName,'r', buffering=100)
    res = inFile.readlines()
    inFile.close()
    return res

def writeFile(data):
    file = open("dataset.csv", "w")
    file.write(data)
    file.close()


def processMiRNAToList(): 

    mirnaCodesList = set()
    data = readFile("mirna-codes.txt")
    for line in data:  
        mirnaCodesList.add(line.strip())

    return mirnaCodesList

def processDatasetClinical(neo4jSession, mongoDb): 

    mirnaCodesSet = processMiRNAToList() 
    lines = ""
    test = ""
    for c in mirnaCodesSet:
        test += c + ","
    lines += test.rstrip(',') + "\n"
    i = 0
    for clinicalDocument in mongoDb.clinical.find():
        if i > 200:
            break
        i+=1

        query = "MATCH (:Clinical { name: '" + clinicalDocument["Case ID"] + "' })-[m]->(r) RETURN m.reads_per_million, r.name"        
        res = neo4jSession.run(query, parameters={})

        inMIRNA = {}
        for record in res:
            inMIRNA[record["r.name"]] =  record["m.reads_per_million"]
        if len(inMIRNA) == 0:
            continue

        line = ""
        for el in mirnaCodesSet:        
            if el  in inMIRNA:
               line += inMIRNA[el] + ","
            else :
                line += "0,"
        #print(line)
        lines += line.rstrip(',') + "\n"   

    writeFile(lines)
  
import pandas as pd
from sklearn.cluster import KMeans

def loadDataset():
    data = pd.read_csv(filepath_or_buffer = 'dataset.csv', sep = ",")
    
    print(data.columns)
    bunch = Bunch(data=data, feature_names=data.columns)
    #print(bunch)
    return bunch


def cluster_k_means():
     bunch = loadDataset()
     estimator = KMeans(init='k-means++', n_clusters=10)
     estimator.fit(bunch.data)
     print(estimator.labels_)
  
     return estimator

def main():
    driver = GraphDatabase.driver(
    "bolt://34.224.17.173:35394", 
    auth=basic_auth("neo4j", "jewel-tuesdays-payment"))

    session = driver.session()

    client = MongoClient("mongodb://localhost:27017")
    mongodb = client.test

    #processDatasetClinical(session, mongodb)

    cluster_k_means()

    session.close()
    client.close()
    

if __name__ == '__main__':
    main()    