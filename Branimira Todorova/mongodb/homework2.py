from pymongo import MongoClient 

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

def processFile2(fileName, db): 
    data = readFile(fileName)
    columns = data[0].split(",")
    length = len(columns)
    countriesDic = {}
    for line in data[1:]:
        keys = line.split(",")
        country = keys[0].split('-')[0].rstrip()

        if len(keys) > 5:
            date = keys[1]
            total = try_to_parse_num(keys[5])
            daily = try_to_parse_num(keys[6])
            if country == 'Japan':
                total = keys[-4]
                daily = keys[-3]

            db.covid19.find_one_and_update({ 'country': country }, 
                                        { "$addToSet": { "stats" : 
                                            {   "date" : date, 
                                                "total" : total, 
                                                "daily" : daily }
                                        }})
       
    

def processFile(fileName, db): 
    data = readFile(fileName)
    columns = data[0].split(",")
    length = len(columns)
    for line in data[1:]:
        keys = line.split(",")
        pop = keys[length - 1].rstrip()
        obj = { "country" :  keys[0], "population" : try_to_parse_num(pop)}
        db.covid19.insert_one(obj)

def main():

    client = MongoClient("mongodb://localhost:27017")
    db = client.test
    
    processFile("locations.csv", db)
    processFile2("covid-testing-05-Apr-all-observations.csv", db)
    
    print("Done")

if __name__ == '__main__':
    main()
