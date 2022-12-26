MATCH (parentProcess:Process),(childProcess:Process) WHERE parentProcess.ProcessId = childProcess.ParentProcessId
CREATE (parentProcess)-[r_process:HAS_CREATED]->(childProcess)