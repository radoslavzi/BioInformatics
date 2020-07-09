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
from sklearn import preprocessing

def loadDataset():
    data = pd.read_csv(filepath_or_buffer = 'dataset.csv', sep = ",")
    
    print(data.columns)
    bunch = Bunch(data=data, feature_names=data.columns)
    #print(bunch)
    return bunch


def cluster_k_means():
     bunch = loadDataset()
     estimator = KMeans(init='k-means++', n_clusters=10)
     kfit = estimator.fit(bunch.data)
     print(estimator.labels_)
     identified_clusters = kfit.predict(bunch.data)
     print(identified_clusters)
     bunch.data['Clusters'] = identified_clusters
     print(bunch.data.sort_values(by='Clusters'))
     return kfit


def cluster_k_means_scaled():
    #Passing the values of the dataset to Min-Max-Scaler
    bunch = loadDataset()
    data_values = bunch.data.values
    print(data_values)
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(data_values)
    data_scaled = pd.DataFrame(x_scaled, columns=bunch.data.columns)

    kmeans = KMeans(init='k-means++', n_clusters=10)
    kfit = kmeans.fit(data_scaled)
    identified_clusters_scaled = kfit.predict(data_scaled)#Appending the identified clusters to the dataframe
    clustered_data_scaled = bunch.data
    clustered_data_scaled['Cluster'] = identified_clusters_scaled
    
    print(clustered_data_scaled.sort_values(by='Cluster'))
    return kfit

def main():
    driver = GraphDatabase.driver(
    "bolt://34.224.17.173:35394", 
    auth=basic_auth("neo4j", "jewel-tuesdays-payment"))

    session = driver.session()

    client = MongoClient("mongodb://localhost:27017")
    mongodb = client.test

    #processDatasetClinical(session, mongodb)

    #cluster_k_means()
    cluster_k_means_scaled()

    session.close()
    client.close()
    

if __name__ == '__main__':
    main()    