from neo4j import GraphDatabase, basic_auth
import sys
import os


class Neo4jPatientsMutationsImporter:
    def __init__(self, session):
        self.session = session

    def run_queries(self, query_generator):
        for query in query_generator:
            self.session.run(query)

    def input_data(self, file_path, name):
        with open(file_path, 'r') as csvfile:
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

    def relate_patient_and_hugo_symbol(self, file_path):
        with open(file_path, 'r') as csvfile:
            lines = csvfile.readlines()
            for line in lines[1:]:
                query = "MATCH (a:Patient),(b:HugoSymbol) "
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


def main(argv):
    driver = GraphDatabase.driver(
        "neo4j://localhost:7687",
        auth=basic_auth("neo4j", "password"),
        encrypted=False)
    main_dir = os.path.dirname(argv[0]) if os.path.dirname(argv[0]) else "."
    data_dir = main_dir + "/../../../Lectures/SEMESTER_2/neo4j/data_integration/test_data"

    print("Importing data from %s directory" % data_dir)
    with driver.session() as session:

        importer = Neo4jPatientsMutationsImporter(session)
        print("Importing Patients' data...")
        importer.run_queries(importer.input_data(data_dir + "/Sample.csv",
                                                 "Patient"))
        print("Importing HugoSymbol...")
        importer.run_queries(importer.input_data(data_dir + "/HugoSymbol.csv",
                                                 "HugoSymbol"))
        print("Importing Patients' mutations...")
        importer.run_queries(importer.relate_patient_and_hugo_symbol(data_dir + "/mutation.csv"))

    print("Importing done.")
    print("Visualise imported data with the following CQL: MATCH (a:Patient)--(b:HugoSymbol) RETURN a, b LIMIT 20")


if __name__ == "__main__":
    main(sys.argv)
