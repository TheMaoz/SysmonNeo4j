import os
import platform
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
        query = """match (n) detach delete (n)"""
        session = self.driver.session()
        session.run(query)
        print("\nPrevious Data have been deleted.")

        self.clearSchema()
        print("\nDatabase is clear and ready for imports.")

    # Clear Schema
    def clearSchema(self):
        # Clear Database from existing constraints and indexes
        query = """CALL apoc.cypher.runSchemaFile("ClearConstraintsIndexes.cypher")"""
        session = self.driver.session()
        session.run(query)
        print("\nPrevious Schema has been deleted.")

    # Constraints and Indexes
    def schema_script(self):
        # Create Constraints and Indexes
        query = """CALL apoc.cypher.runSchemaFile("ConstraintsIndexes.cypher")"""
        session = self.driver.session()
        session.run(query)
        print("\nSchema with Constraints and Indexes insertion completed.")

# Copy Cypher Script files to Import Path
# Define Dataset Files in them
def replace_files_cypher_script(files):
    stringToInsert = "\""
    for file in files:
        stringToInsert += file + "\", \""
    stringToInsert = stringToInsert[:-3]

    current_path = os.getcwd()
    current_os = platform.system()
    if current_os == "Linux":
        current_path += "/CypherScripts/"
    elif current_os == "Windows":
        current_path += "\CypherScripts\\"

    if stringToInsert.startswith("\"nvdcpe"):
        toUpdate = current_path + "CPEs.cypher"
        fin = open(toUpdate, "rt")
        updatedFile = import_path + "CPEs.cypher"
        fout = open(updatedFile, "wt")
        for line in fin:
            fout.write(line.replace('filesToImport', stringToInsert))
        fin.close()
        fout.close()
    elif stringToInsert.startswith("\"nvdcve"):
        toUpdate = current_path + "CVEs.cypher"
        fin = open(toUpdate, "rt")
        updatedFile = import_path + "CVEs.cypher"
        fout = open(updatedFile, "wt")
        for line in fin:
            fout.write(line.replace('filesToImport', stringToInsert))
        fin.close()
        fout.close()
    elif stringToInsert.startswith("\"cwe"):
        toUpdate = current_path + "CWEs.cypher"
        fin = open(toUpdate, "rt")
        updatedFile = import_path + "CWEs.cypher"
        fout = open(updatedFile, "wt")
        for line in fin:
            fout.write(line.replace('filesToImport', stringToInsert))
        fin.close()
        fout.close()
    elif stringToInsert.startswith("\"capec"):
        toUpdate = current_path + "CAPECs.cypher"
        fin = open(toUpdate, "rt")
        updatedFile = import_path + "CAPECs.cypher"
        fout = open(updatedFile, "wt")
        for line in fin:
            fout.write(line.replace('filesToImport', stringToInsert))
        fin.close()
        fout.close()


# Copy Cypher Script Schema Files to Import Path
def copy_files_cypher_script():
    current_path = os.getcwd()
    current_os = platform.system()
    if current_os == "Linux":
        current_path += "/CypherScripts/"
    elif current_os == "Windows":
        current_path += "\CypherScripts\\"

    shutil.copy2(current_path + "ConstraintsIndexes.cypher", import_path)
    shutil.copy2(current_path + "ClearConstraintsIndexes.cypher", import_path)


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
