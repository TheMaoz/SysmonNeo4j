MATCH (process:Process),(ip:Ip) WHERE process.ProcessId = ip.ProcessId
CREATE (process)-[n_network:COMMUNICATED_WITH]->(ip)