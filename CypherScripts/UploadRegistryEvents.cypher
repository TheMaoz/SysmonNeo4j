CALL apoc.load.json($file) YIELD value AS RegistryKey
MERGE (n:RegistryKey {TargetObject: RegistryKey.TargetObject})
SET n.Pid = RegistryKey.PID
SET n.Image = RegistryKey.Image
SET n.TargetObject = RegistryKey.TargetObject
SET n.EventType = RegistryKey.EventType
SET n.User = RegistryKey.User
SET n.UtcTime = RegistryKey.UtcTime
