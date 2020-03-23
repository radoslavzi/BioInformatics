from neo4j.v1 import GraphDatabase, basic_auth
import sys

def main(url, name):
    with open(url, 'r') as csvfile:
        lines = csvfile.readlines()
        for line in lines[1:]:
            query = "CREATE (a:{}) ".format(name)
            keys = line.split(",")
            for key in keys:
                key_value = key.split(":")
                if len(key_value) == 2:
                    query += " SET a." + \
                        key_value[0].rstrip() + " = '" + \
                        key_value[1].rstrip() + "' "
            query += " RETURN a"
            yield query
    pass


def create_relation():
    with open('test_data/mutation.csv', 'r') as csvfile:
        lines = csvfile.readlines()
        for line in lines[1:]:
            query = "MATCH (a:sample),(b:hugosymbol) "
            keys = line.split(",")
            query += "WHERE a.name = '{}' AND b.name = '{}' CREATE (a)-[r:mutation]->(b) ".format(
                keys[0].rstrip(), keys[len(keys) - 1].rstrip())
            for key in keys[1:len(keys)-1]:
                key_value = key.split(":")
                if len(key_value) >= 2:
                    query += " SET r.{} = '{}' ".format(
                        key_value[0].rstrip(), key_value[1].rstrip())
            query += " RETURN a"
            yield query
    return


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Enter valid url, user name and password")
        exit()

    url = str(sys.argv[1])
    userName = str(sys.argv[2])
    password = str(sys.argv[3])
    type = sys.argv[4]

    driver = GraphDatabase.driver(url, auth=basic_auth(userName, password))
    _session = driver.session()

    print("Authentication si success")

    index = 0
    if type == "sample":
        iterator = main('test_data/Sample.csv', "sample")
        for query in iterator:
            index = index + 1
            print("Add new entry in sample index = {}".format(index))
            res = _session.run(query)
        
        exit()
    
    index = 0
    if type == "hugosymbol":
        iterator = main('test_data/HugoSymbol.csv', "hugosymbol")
        for query in iterator:
            index = index + 1
            print("Add new entry in hugosymbol index = {}".format(index))
            res = _session.run(query)

        exit()
    
    index = 0
    if type == "mutations":
        itrator = create_relation()
        for query in itrator:
            index = index + 1
            print("Add new relations index = {}".format(index))
            res = _session.run(query)
        exit()
