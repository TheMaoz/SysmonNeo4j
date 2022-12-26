CALL apoc.load.json($file) YIELD value AS file
MERGE (n:File {TargetFilename: file.TargetFilename})
SET n.CreationUtcTime = file.CreationUtcTime
SET n.Image = file.Image
SET n.ProcessGuid = file.ProcessGuid
SET n.ProcessId = file.ProcessId
SET n.RuleName = file.RuleName
SET n.TargetFilename = file.TargetFilename
SET n.User = file.User
SET n.CreationTime = file.UtcTime
SET n.DeletionTime = file.EndUTCTime
SET n.Description = file.Description