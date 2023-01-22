import os
from pathlib import Path
from neo4j import GraphDatabase

class App:
    # Initializing the Neo4j Driver.
    def __init__(self, url, username, password):
        self.driver = GraphDatabase.driver(url, auth=(username, password))
        self.import_dir = self.set_import_dir()
    
    # Set the DBMS import directory.
    def set_import_dir(self):
        session = self.driver.session()
        result = session.run(
            "Call dbms.listConfig() YIELD name, value WHERE name='server.directories.import' RETURN value")
        return [record["value"] for record in result][0]

    # Don't forget to close the driver connection when you are finished with it
    def close(self):
        self.driver.close()

    # Clear the database.
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
        upload_query_path = Path(
            Path.cwd(), "CypherScripts", "UploadProcessEvents.cypher")
        with open(upload_query_path, encoding='utf-8') as file:
            upload_query = file.read()
        session.run(upload_query, file=processes_json_path)
        print("\nProcess events insertion completed.")

    # Files - Event id 11, 23, 26.
    def upload_files_events(self):
        session = self.driver.session()
        files_json_path = "files.json"
        upload_query_path = Path(
            Path.cwd(), "CypherScripts", "UploadFileEvents.cypher")
        with open(upload_query_path, encoding='utf-8') as file:
            upload_query = file.read()
        session.run(upload_query, file=files_json_path)
        print("\nFile events insertion completed.")

    # Registry - Event id 12, 13, 14.
    def upload_registry_events(self):
        session = self.driver.session()
        registry_json_path = "registry.json"
        upload_query_path = Path(
            Path.cwd(), "CypherScripts", "UploadRegistryEvents.cypher")
        with open(upload_query_path, encoding='utf-8') as file:
            upload_query = file.read()
        session.run(upload_query, file=registry_json_path)
        print("\nRegistry events insertion completed.")

    # Network - Event id 3.
    def upload_network_events(self):
        session = self.driver.session()
        network_json_path = "network.json"
        upload_query_path = Path(
            Path.cwd(), "CypherScripts", "UploadNetworkEvents.cypher")
        with open(upload_query_path, encoding='utf-8') as file:
            upload_query = file.read()
        session.run(upload_query, file=network_json_path)
        print("\nNetwork events insertion completed.")

    def set_nodes_relationship(self):
        """This function run Cyphers that set the relationship between the nodes"""
        session = self.driver.session()
        relation_queries_path = Path(
            Path.cwd(), "CypherScripts", "RelationsCyphers")
        query_paths = (relation_queries_path.iterdir())

        # Run each relation query.
        for query_path in query_paths:
            with open(query_path, encoding='utf-8') as file:
                session.run(file.read())
        print("\nNodes relationship has been set.")

    # Clear DBMS import directory.
    def clear_import_directory(self):
        """Clear the DBMS import dir"""
        for file in os.listdir(self.import_dir):
            os.remove(os.path.join(self.import_dir, file))
