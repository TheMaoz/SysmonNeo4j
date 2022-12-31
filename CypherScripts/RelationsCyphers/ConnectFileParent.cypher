MATCH (process:Process),(file:File) WHERE process.ProcessId = file.ProcessId
CREATE (process)-[r_file:ACCESSED_FILE]->(file)