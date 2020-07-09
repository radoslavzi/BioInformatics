from pymongo import MongoClient
import sys
import os
import csv


def convert_int(row, key):
    if row[key]:
        row[key] = int(row[key])


def main(argv):
    client = MongoClient('localhost')
    db = client.test

    print("Authentication is success")
    main_dir = os.path.dirname(argv[0]) if os.path.dirname(argv[0]) else "."
    data_dir = main_dir + "/../../../Lectures/SEMESTER_2/COVID-19/data"

    with open(data_dir + "/locations.csv") as csvfile:
        locations_reader = csv.DictReader(csvfile)
        for row in locations_reader:
            convert_int(row, 'population_year')
            convert_int(row, 'population')
            db.locations.insert_one(row)

    with open(data_dir + "/covid-testing-05-Apr-all-observations.csv") as csvfile:
        countries_reader = csv.DictReader(csvfile)
        for row in countries_reader:
            country = row['Entity'].split(' ')[0].lower()
            result = db['location_' + country].find_one({'Date': row['Date']})
            if not result:
                db['location_' + country].insert_one(row)


if __name__ == "__main__":
    main(sys.argv)
