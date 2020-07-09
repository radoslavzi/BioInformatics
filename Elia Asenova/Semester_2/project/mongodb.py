from pymongo import MongoClient
import pandas as pd
import json
import csv

def read_tsv_file_to_json(filePath):
    with open(filePath, "r") as tsvFile:
        data = pd.read_csv(tsvFile, delimiter="\t")
        data_json = json.loads(data.to_json(orient='records'))

        return data_json

def read_data_to_db(db, filePath, collection, propertyTuple = None):
    data_json = read_tsv_file_to_json(filePath)
    if propertyTuple is not None:
        add_property_to_json(propertyTuple, data_json)
    
    db[collection].insert_many(data_json)

def read_files_in_folders(db, fromFile):
    data_json = read_tsv_file_to_json(fromFile)
    i = 0
    while i < len(data_json):
        fileId = data_json[i]['File ID']
        fileName = data_json[i]['File Name']
        dataCategory = data_json[i]['Data Category']
        dataType = data_json[i]['Data Type']
        caseIdTuple = ['Case ID', data_json[i]['Case ID']]

        folderAndCollection = map_category_to_folder_name(dataCategory, dataType)
        if folderAndCollection is not None:
            if folderAndCollection[0] != "skip":
                read_data_to_db(db, "data/" + folderAndCollection[0] + "/" + fileId + "/" + fileName, folderAndCollection[1], caseIdTuple)

        i += 1

def map_category_to_folder_name(dataCategory, dataType):
    if dataCategory == 'Copy Number Variation':
        if dataType == 'Copy Number Segment':
            return ["cnv_segments", "Copy Number Variation"]
        elif dataType == 'Masked Copy Number Segment':
            return ["masked_cnv_segments", "Masked Copy Number Variation"]
    elif dataCategory == 'Transcriptome Profiling' and "miRNA" in dataType:
        return ["mirnas_gdc", "miRNA Expression"]
    else:
        return ["skip"]

def add_property_to_json(propertyTuple, json_data):
    for el in json_data:
        el[propertyTuple[0]] = propertyTuple[1]

def main():
    client = MongoClient('localhost', 27017)
    db = client.breast_cancer

    read_data_to_db(db, "data/clinical_data/clinical.tsv", "clinical")
    # read_files_in_folders(db, "data/gdc_sample_sheet.tsv")

if __name__ == "__main__":
    main()
