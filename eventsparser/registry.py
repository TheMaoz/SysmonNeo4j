import json
from app import write_json

# ToDo: Chcek for diffrence between id 12,13,14.

def registry_events_insertion(registry_events):
    """
    This function recives a list of registry events (id 12&13),
    parse it and save the output to the DBMS import directory.
    """
    registry = []
    for event in registry_events:
        event_id = event['Event']['System']['EventID']
        if event_id == 12:
            desc = "Key or value were created or deleted."
        elif event_id == 13:
            desc = "Key value was set."
        elif event_id == 14:
            desc = "Key or value were renamed."
        event_data = event['Event']['EventData']
        event_data.update({"Description": desc})
        registry.append(event_data)
    write_json(registry, "registry")
