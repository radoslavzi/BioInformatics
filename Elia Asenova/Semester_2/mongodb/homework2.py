from pymongo import MongoClient
import pandas as pd
import json
import csv


def read_data_to_db(db, filePath, collection):
    with open(filePath, "r") as csvFile:
        data = pd.read_csv(csvFile)
        data_json = json.loads(data.to_json(orient='records'))

        if collection == "test":
            modify_json(data_json)

        db[collection].insert_many(data_json)


def modify_json(data_json):
    for data in data_json:
        source = {}
        source["URL"] = data["Source URL"]
        source["label"] = data["Source label"]
        data["Source"] = source
        data.pop("Source URL")
        data.pop("Source label")


def create_relation(db, fromCollection, toCollection, criteria, findColumn, updateColumn):
    for doc in db[fromCollection].find({}, criteria):
        db[toCollection].update_many(
            {findColumn: {"$regex": ".*" + doc["location"] + ".*"}}, {"$set": {updateColumn: doc["_id"]}})


def main():
    client = MongoClient('localhost', 27017)
    db = client.covid

    read_data_to_db(db, "data/locations.csv", "countries")
    read_data_to_db(
        db, "data/covid-testing-05-Apr-all-observations.csv", "test")

    create_relation(db, "countries", "test",
                    {"location": 1}, "Entity", "Country_id")


if __name__ == "__main__":
    main()
