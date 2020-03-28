from neo4j import GraphDatabase, basic_auth


def readFile(inFileName):
    inFile = open(inFileName,'r', buffering=100)
    res = inFile.readlines()
    inFile.close()
    return res



def processNodes(fileName, session): 
    first = readFile(fileName + ".csv")
    for line in first[1:]:
        query = "CREATE (a:" + fileName
        keys = line.split(",")
        options = ""
        for key in keys:
                key_value = key.rstrip().split(":")
                options +=  key_value[0] + ": \'" + key_value[1] + "\',"        
        query += " { " + options[0:len(options)-1] + "} )"
        
        #print(query)     
        session.run(query, parameters={})
   

def processVertex(fileName, session): 
    first = readFile(fileName + ".csv")
    for line in first[1:]:
        
        query = "MATCH (a:Sample),(b:HugoSymbol)"
        keys = line.rstrip().split(",")
        last = len(keys)-1
        query += " WHERE a.name = '" + keys[0] + "' AND b.name = '" + keys[last] + "'"
        query += " CREATE (a)-[r:mutation]->(b)"
        options = {}
        for key in keys[1:last]:
                key_value = key.rstrip().split(":") 
                if len(key_value) >= 2:
                    query += " SET r." + key_value[0] + "='" + key_value[1] + "'"
     
        #print(query) 
        session.run(query, parameters={})
        

     
def main():
    driver = GraphDatabase.driver(
    "bolt://100.25.45.169:33374", 
    auth=basic_auth("neo4j", "age-driver-nomenclatures"))
    session = driver.session()
    #processNodes("HugoSymbol", session)
    #processNodes("Sample", session)

    #processVertex("mutation", session)


    

if __name__ == "__main__":
    main()
