CALL apoc.load.json('events.json') YIELD value AS process
MERGE (p:Process {pid: process.PID})
SET p.ppid = process.PPID
SET p.pid = process.PID
SET p.image = process.Image
SET p.filename = process.FileName
SET p.cmdline = process.CommandLine
SET p.username = process.Username
SET p.StartTime = process.StartTime
SET p.EndTime = process.EndTime
