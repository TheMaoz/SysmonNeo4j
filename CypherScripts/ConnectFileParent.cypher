MATCH (process_file:Process),(childFile:File) WHERE process_file.ProcessId = childFile.ProcessId
CREATE (process_file)-[r_file:ACCESSED_FILE]->(childFile)