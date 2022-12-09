MATCH (parent:Process),(child:Process) WHERE parent.pid = child.ppid
CREATE (parent)-[r:HAS_CREATED]->(child)
RETURN type(r)