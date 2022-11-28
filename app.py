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

    # Cypher Query to insert CPE Cypher Script
    def query_cpe_script(self, files):
        # Insert file with CPE Query Script to Database
        query = """CALL apoc.cypher.runFile("CPEs.cypher")"""
        session = self.driver.session()
        session.run(query)
        for file in files:
            print("\nCPE Files: " + file + " insertion completed. \n----------")

    # Configure CPE Files and CPE Cypher Script for insertion
    def cpe_insertion(self):
        print("\nInserting CPE Files to Database...")
        files = files_to_insert_cpe()
        for f in files:
            print('Inserting ' + f)
        self.query_cpe_script(files)

    # Cypher Query to insert CVE Cypher Script
    def query_cve_script(self, files):
        query = """CALL apoc.cypher.runFile("CVEs.cypher")"""
        session = self.driver.session()
        session.run(query)
        for file in files:
            print("\nCVE Files: " + file + " insertion completed. \n----------")

    # Configure CVE Files and CVE Cypher Script for insertion
    def cve_insertion(self):
        print("\nInserting CVE Files to Database...")
        files = files_to_insert_cve()
        for f in files:
            print('Inserting ' + f)
        self.query_cve_script(files)

    # Cypher Query to insert CWE Cypher Script
    def query_cwe_script(self, files):
        query = """CALL apoc.cypher.runFile("CWEs.cypher")"""
        session = self.driver.session()
        session.run(query)
        for file in files:
            print("\nCWE Files: " + file + " insertion completed. \n----------")

    # Configure CWE Files and CWE Cypher Script for insertion
    def cwe_insertion(self):
        print("\nInserting CWE Files to Database...")
        files = files_to_insert_cwe()
        for f in files:
            print('Inserting ' + f)
        self.query_cwe_script(files)

    # Cypher Query to insert CAPEC Cypher Script
    def query_capec_script(self, files):
        query = """CALL apoc.cypher.runFile("CAPECs.cypher")"""
        session = self.driver.session()
        session.run(query)
        for file in files:
            print("\nCAPEC Files: " + file + " insertion completed. \n----------")

    # Configure CAPEC Files and CAPEC Cypher Script for insertion
    def capec_insertion(self):
        print("\nInserting CAPEC Files to Database...")
        files = files_to_insert_capec()
        for f in files:
            print('Inserting ' + f)
        self.query_capec_script(files)


# Define which Dataset and Cypher files will be imported on CPE Insertion
def files_to_insert_cpe():
    listOfFiles = os.listdir(import_path)
    pattern = "*.json"
    files = []
    for entry in listOfFiles:
        if fnmatch.fnmatch(entry, pattern):
            if entry.startswith("nvdcve") or entry.startswith("capec") or entry.startswith("cwe"):
                continue
            files.append(entry)
    replace_files_cypher_script(files)
    return files


# Define which Dataset and Cypher files will be imported on CVE Insertion
def files_to_insert_cve():
    listOfFiles = os.listdir(import_path)
    pattern = "*.json"
    files = []
    for entry in listOfFiles:
        if fnmatch.fnmatch(entry, pattern):
            if entry.startswith("nvdcpe") or entry.startswith("capec") or entry.startswith("cwe"):
                continue
            files.append(entry)
    replace_files_cypher_script(files)
    return files


# Define which Dataset and Cypher files will be imported on CWE Insertion
def files_to_insert_cwe():
    listOfFiles = os.listdir(import_path)
    pattern = "*.json"
    files = []
    for entry in listOfFiles:
        if fnmatch.fnmatch(entry, pattern):
            if entry.startswith("nvdcpe") or entry.startswith("capec") or entry.startswith("nvdcve"):
                continue
            files.append(entry)
    replace_files_cypher_script(files)
    return files


# Define which Dataset and Cypher files will be imported on CAPEC Insertion
def files_to_insert_capec():
    listOfFiles = os.listdir(import_path)
    pattern = "*.json"
    files = []
    for entry in listOfFiles:
        if fnmatch.fnmatch(entry, pattern):
            if entry.startswith("nvdcpe") or entry.startswith("cwe") or entry.startswith("nvdcve"):
                continue
            files.append(entry)
    replace_files_cypher_script(files)
    return files


# Convert XML Files to JSON Files
def xml_to_json():
    # parse the import folder for xml files
    # open the input xml file and read
    # data in form of python dictionary
    # using xmltodict module
    for file in os.listdir(import_path):
        if file.endswith(".xml"):
            with open(import_path + f'{file}', encoding="utf8") as xml_file:
                data_dict = xmltodict.parse(xml_file.read())
                xml_file.close()
                # generate the object using json.dumps()
                # corresponding to json data
                json_data = json.dumps(data_dict)
                # Write the json data to output
                # json file
                jsonfile = import_path + f'{file}'
                jsonfile = jsonfile.replace(".xml", ".json")
                with open(jsonfile, "w") as json_file:
                    json_file.write(json_data)
                    json_file.close()
                os.remove(import_path + f'{file}')


# Flatten CWE Dataset File
def replace_unwanted_string_cwe():
    listOfFiles = os.listdir(import_path)
    pattern = "*.json"
    files = []
    for entry in listOfFiles:
        if fnmatch.fnmatch(entry, pattern):
            if entry.startswith("cwec"):
                files.append(entry)
                break
    file = import_path + files[0]
    fin = open(file, "rt")
    flattened_cwe = import_path + "cwe.json"
    fout = open(flattened_cwe, "wt")
    for line in fin:
        fout.write(line.replace('"@', '"'))
    fin.close()
    os.remove(file)
    fout.close()


# Flatten CAPEC Dataset File
def replace_unwanted_string_capec():
    listOfFiles = os.listdir(import_path)
    pattern = "*.json"
    files = []
    for entry in listOfFiles:
        if fnmatch.fnmatch(entry, pattern):
            if entry.startswith("capec"):
                files.append(entry)
                break
    file = import_path + files[0]
    fin = open(file, "rt")
    flattened_cwe = import_path + "capec.json"
    fout = open(flattened_cwe, "wt")
    for line in fin:
        fout.write(line.replace('"@', '"').replace('#text', 'text'))
    fin.close()
    fout.close()
    os.remove(file)


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
