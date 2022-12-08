//CALL apoc.load.json("file://$path") YIELD value AS process
//CALL apoc.convert.fromJsonList($list) YIELD value AS process
WITH apoc.convert.fromJsonList($list) AS processes
UNWIND processes as process
MERGE (p:Process {pid: process.PID})
SET p.ppid = process.PPID
SET p.pid = process.PID
SET p.image = process.Image
SET p.filename = process.FileName
SET p.cmdline = process.CommandLine
SET p.username = process.Username
SET p.StartTime = process.StartTime
SET p.EndTime = process.EndTime
