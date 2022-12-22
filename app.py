import os
import platform
import shutil
import json
from neo4j import GraphDatabase



class App:

    # Initializing Neo4j Driver
    def __init__(self, url, username, password):
        self.driver = GraphDatabase.driver(url, auth=(username, password))

    def set_import_dir(self):
        global import_dir
        session = self.driver.session()
        result = session.run("Call dbms.listConfig() YIELD name, value WHERE name='server.directories.import' RETURN value")
        import_dir = [record["value"] for record in result][0]


    # Don't forget to close the driver connection when you are finished with it
    def close(self):
        self.driver.close()

    # Clear Database
    def clear(self):
        # Clear Database from existing nodes and relationships
        query = """MATCH (n) optional MATCH (n)-[r]-() DELETE n,r"""
        session = self.driver.session()
        session.run(query)
        print("\nPrevious Data have been deleted.")
        print("\nDatabase is clear and ready for imports.")

    # Processes - Event id 1 & 5.
    def upload_processes(self):
        session = self.driver.session()
        processes_json_path ="processes.json"
        upload_query = open(f"CypherScripts/UploadProcess.cypher").read()
        session.run(upload_query, file=processes_json_path)
        connect_query = open(f"CypherScripts/ConnectProcessParent.cypher").read()
        session.run(connect_query)
        print("\nProcess insertion completed.")


def write_json(data, event_type):
    """
    :param data: json list of events (processes/registry/files/etc)
    :param event_type: (to defer which .json is created) processes,files...
    write data to .json in import folder.
    :TODO: clear event_type.json if exists
    """
    with open(import_dir+"\\"+event_type + ".json", "w") as write:
        json.dump(data, write)


# Clear events Directory
def clear_directory():
    for f in os.listdir(import_dir):
        os.remove(os.path.join(import_dir, f))
