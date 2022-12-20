import os
import platform
import shutil
import json
from neo4j import GraphDatabase
global events_folder
events_folder = ".\\CypherScripts\\events\\"

class App:

    # Initializing Neo4j Driver
    def __init__(self, url, username, password):
        self.driver = GraphDatabase.driver(url, auth=(username, password))


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
        #                                         remove .   remove 'c:'
        processes_json_path = (os.getcwd()+events_folder[1::])[2::]+"\\processes.json"
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
    if not os.path.exists(events_folder):
        os.mkdir(events_folder)
    with open(os.getcwd()+events_folder+event_type + ".json", "w") as write:
        json.dump(data, write)


# Clear events Directory
def clear_directory():
    if os.path.exists(events_folder):
        for f in os.listdir(events_folder):
            os.remove(os.path.join(events_folder, f))
