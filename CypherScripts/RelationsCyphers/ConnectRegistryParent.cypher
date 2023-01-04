MATCH (process:Process),(registry:RegistryKey) WHERE process.ProcessId = registry.ProcessId
CREATE (process)-[r_registry:ACCESSED_REGISTRY]->(registry)