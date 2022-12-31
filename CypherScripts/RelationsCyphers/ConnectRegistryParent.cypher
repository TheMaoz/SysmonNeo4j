MATCH (process:Process),(Registry:RegistryKey) WHERE process.ProcessId = Registry.ProcessId
CREATE (process)-[r_registry:ACCESSED_REGISTRY]->(Registry)