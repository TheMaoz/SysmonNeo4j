CALL apoc.load.json($file) YIELD value AS RegistryKey
MERGE (n:RegistryKey {TargetObject: RegistryKey.TargetObject})
SET n.Details = RegistryKey.Details
SET n.EventType = RegistryKey.EventType
SET n.Image = RegistryKey.Image
SET n.ProcessGuid = RegistryKey.ProcessGuid
SET n.ProcessId = RegistryKey.ProcessId
SET n.RuleName = RegistryKey.RuleName
SET n.TargetObject = RegistryKey.TargetObject
SET n.User = RegistryKey.User
SET n.UtcTime = RegistryKey.UtcTime
SET n.NewName = RegistryKey.NewName
SET n.Description = RegistryKey.Description
