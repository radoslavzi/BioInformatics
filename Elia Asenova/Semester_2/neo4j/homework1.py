from neo4j import GraphDatabase, basic_auth

driver = GraphDatabase.driver(
    "bolt://54.208.66.5:36826",
    auth=basic_auth("neo4j", "lesson-centers-sips"))
session = driver.session()


def input_data(filePath, name):
    with open(filePath, "r") as csvFile:
        line = csvFile.readline()
        while line:
            properties = line.split(',')
            query = "CREATE (a:{})".format(name)
            for property in properties:
                property_tuple = property.split(':')
                if len(property_tuple) == 2:
                    query += " SET a." + \
                        property_tuple[0].rstrip() + " = '" + \
                        property_tuple[1].rstrip() + "'"
            query += " RETURN a"
            session.run(query)
            line = csvFile.readline()


def create_relations(filePath, fromEntity, toEntity, name):
    with open(filePath, "r") as csvFile:
        line = csvFile.readline()
        while line:
            properties = line.split(',')
            query = "MATCH (a:{}),(b:{}) WHERE a.name='{}' and b.name='{}' CREATE (a)-[r:{}]->(b)".format(
                fromEntity, toEntity, properties[0].rstrip(), properties[len(properties) - 1].rstrip(), name)
            for i in range(1, len(properties)-1):
                property_tuple = properties[i].split(':')
                if len(property_tuple) >= 2:
                    query += " SET r." + \
                        property_tuple[0].rstrip() + " = '" + \
                        property_tuple[1].rstrip() + "'"
            session.run(query)
            line = csvFile.readline()


def main():
    input_data("data/Sample.csv", "Sample")
    # input_data("data/HugoSymbol.csv","HugoSymbol")
    # create_relations("data/mutation.csv", "Sample", "HugoSymbol", "MUTATION")


if __name__ == "__main__":
    main()
