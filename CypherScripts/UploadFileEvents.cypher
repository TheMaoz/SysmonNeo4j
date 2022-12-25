CALL apoc.load.json($file) YIELD value AS file
MERGE (n:File {TargetFilename: file.TargetFilename})
SET n.Pid = file.PID
SET n.Image = file.Image
SET n.TargetFilename = file.TargetFilename
SET n.CreationUtcTime = file.CreationUtcTime
SET n.User = file.User
SET n.UtcTime = file.UtcTime
