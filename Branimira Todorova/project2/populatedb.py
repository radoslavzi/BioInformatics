from pymongo import MongoClient 
import os

def readFile(inFileName):
    inFile = open(inFileName,'r', buffering=100)
    res = inFile.readlines()
    inFile.close()
    return res


def try_to_parse_num(s):
    try:
        return int(s)
    except ValueError:
        return s 

def processRecursiveFile(directory, collection): 
    
    for dirr in os.listdir(directory):
        path = os.path.join(directory, dirr)
        print(path)
        if dirr == 'MANIFEST.txt' or dirr == '.DS_Store':
            continue

        for filename in os.listdir(path):   
            #print(os.path.join(path, filename))
            processFile2(os.path.join(path, filename), filename,  collection)
       
def processFile2(fileName, shortFile, collection): 
    data = readFile(fileName)
    columns = data[0].split("\t")
    print(columns)
    length = len(columns)
    arr = []
    for line in data[1:]:
        keys = line.split("\t")
        id = keys[0]
        obj = {}
        i = 0
        for key in keys:
            obj[columns[i]] = key.strip()
            i+=1    
        arr.append(obj)    
    obj1 = { "fileName" : shortFile, columns[0] : id, "data" : arr}   
    #print(obj1) 
    collection.insert_one(obj1)

def processFileUpdateDocument(fileName, collection): 
    data = readFile(fileName)
    columns = data[0].split("\t")
    print(columns)
    length = len(columns)
    for line in data[1:]:
        keys = line.split("\t")
        obj = {}
        i = 0
        for key in keys:
            obj[columns[i]] = key  
            i+=1
        collection.find_one_and_update({ 'Case ID' : keys[1] },
        { 
               "$set" : obj
        })
    

def processFileUpdateDocument2(fileName, collection): 
    data = readFile(fileName)
    columns = data[0].split("\t")
    print(columns)
    length = len(columns)
    for line in data[1:]:
        keys = line.split("\t")
        obj = {}
        i = 1
        for key in keys[1:]:
            obj[columns[i]] = key
            i+=1  
        collection.find_one_and_update({ 'case_id' : keys[0] },
        { 
                "$set" : obj
        })

def processFile(fileName, collection): 
    data = readFile(fileName)
    columns = data[0].split("\t")
    print(columns)
    length = len(columns)
    for line in data[1:]:
        keys = line.split("\t")
        obj = {}
        i = 0
        for key in keys:
            obj[columns[i]] = key
            i+=1
        collection.insert_one(obj)

def main():

    client = MongoClient("mongodb://localhost:27017")
    db = client.test
    
    #processFile("gdc_sample_sheet.2019-02-08.tsv", db.clinical)
    #processFileUpdateDocument("clinical.cart.2019-02-13/clinical.tsv", db.clinical)
    #processFileUpdateDocument2("clinical.cart.2019-02-13/exposure.tsv", db.clinical)

    ##processFile("clinical.cart.2019-02-13/clinical.tsv", db.clinical)
    ##processFileUpdateDocument("clinical.cart.2019-02-13/exposure.tsv", db.clinical)

    #processRecursiveFile("/Users/branimira/Downloads/cnv_segments_download_20190208", db.cnv_segment)
   
    processRecursiveFile("/Users/branimira/Downloads/mirnas_gdc_download_20190208", db.mirna)
    
    print("Done")
    client.close()
    

if __name__ == '__main__':
    main()
