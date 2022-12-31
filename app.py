import os
import json
from neo4j import GraphDatabase
from pathlib import Path


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
        '''Clear Database from existing nodes and relationships'''
        query = """MATCH (n) optional MATCH (n)-[r]-() DELETE n,r"""
        session = self.driver.session()
        session.run(query)
        print("\nPrevious Data have been deleted.")
        print("\nDatabase is clear and ready for imports.")

    # Processes - Event id 1 & 5.
    def upload_processes_events(self):
        session = self.driver.session()
        processes_json_path = "processes.json"
        upload_query_path = Path(Path.cwd(), "CypherScripts", "UploadProcessEvents.cypher")
        with open(upload_query_path, encoding='utf-8') as file:
            upload_query = file.read()
        session.run(upload_query, file=processes_json_path)
        print("\nProcess events insertion completed.")
    
    # Files - Event id 11 & 23.
    def upload_files_events(self):
        session = self.driver.session()
        files_json_path = "files.json"
        upload_query_path = Path(Path.cwd(), "CypherScripts", "UploadFileEvents.cypher")
        with open(upload_query_path, encoding='utf-8') as file:
            upload_query = file.read()
        session.run(upload_query, file=files_json_path)
        print("\nFile events insertion completed.")

    # Registry - Event id 12, 13, 14.
    def upload_registry_events(self):
        session = self.driver.session()
        registry_json_path = "registry.json"
        upload_query_path = Path(Path.cwd(), "CypherScripts", "UploadRegistryEvents.cypher")
        with open(upload_query_path, encoding='utf-8') as file:
            upload_query = file.read()
        session.run(upload_query, file=registry_json_path)
        print("\nRegistry events insertion completed.")


    def set_nodes_relationship(self):
        """This function run Cyphers that set the relationship between the nodes"""
        session = self.driver.session()
        relation_queries_path = Path(Path.cwd(), "CypherScripts", "RelationsCyphers")
        query_paths = (relation_queries_path.iterdir())
        
        # Run each relation query.
        for query_path in query_paths:
            with open(query_path, encoding='utf-8') as file:
                session.run(file.read())
        print("\nNodes relationship has been set.")


def write_json(data, event_type):
    """
    :param data: json list of events (processes/registry/files/etc)
    :param event_type: (to defer which .json is created) processes,files...
    write data to .json in import folder.
    """
    path = (Path(import_dir,event_type)).with_suffix(".json")
    with open(path, "w", encoding='utf-8') as write:
        json.dump(data, write)


# Clear events Directory
def clear_directory():
    for file in os.listdir(import_dir):
        os.remove(os.path.join(import_dir, file))
