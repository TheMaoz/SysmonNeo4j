CALL apoc.load.json($file) YIELD value AS conf
MERGE (n:Config {Description: conf.Description})
SET n.SchemaVersion = conf.SchemaVersion
SET n.State = conf.State
SET n.UtcTime = conf.UtcTime
SET n.ProcessId = conf.ProcessId
SET n.Version = conf.Version
// event id 16
SET n.ConfigurationFile = conf.Configuration
SET n.ConfigurationFileHash = conf.ConfigurationFileHash