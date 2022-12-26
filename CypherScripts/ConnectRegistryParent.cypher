MATCH (process_registry:Process),(childRegistry:RegistryKey) WHERE process_registry.ProcessId = childRegistry.ProcessId
CREATE (process_registry)-[r_registry:ACCESSED_REGISTRY]->(process_registry)