import os
import platform
import shutil
import json
from neo4j import GraphDatabase


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
        # Create Constraints and Indexes
        #upload_query = """CALL apoc.cypher.runSchemaFile("UploadProcess.cypher")"""
        #connect_query = """CALL apoc.cypher.runSchemaFile("ConnectProcessParent.cypher")"""
        upload_query = open(f"{import_path}/UploadProcess.cypher").read()
        connect_query = open(f"{import_path}/ConnectProcessParent.cypher").read()
        session = self.driver.session()
        session.run(upload_query)
        session.run(connect_query)
        print("\nProcess insertion completed.")

# Copy Cypher Script Schema Files to Import Path
def copy_files_cypher_script():
    current_path = os.getcwd()
    current_os = platform.system()
    if current_os == "Linux":
        current_path += "/CypherScripts/"
    elif current_os == "Windows":
        current_path += "\CypherScripts\\"

    shutil.copy2(current_path + "ConnectProcessParent.cypher", import_path)
    shutil.copy2(current_path + "UploadProcess.cypher", import_path)

def write_json(data, event_type):
    """
    :param data: json list of events (processes/registry/files/etc)
    :param event_type: (to defer which .json is created) processes,files...
    write data to .json in project folder.
    :TODO: Create method to copy * to neo4j import folder.
    """
    with open(import_path + event_type + ".json", "w") as write:
        json.dump(data, write)


# Clear Import Directory
def clear_directory():
    for f in os.listdir(import_path):
        os.remove(os.path.join(import_path, f))


# Set Import Directory
def set_import_path(directory):
    global import_path
    current_os = platform.system()
    if current_os == "Linux":
        import_path = directory
    elif current_os == "Windows":
        import_path = directory.replace("\\", "\\\\") + "\\\\"