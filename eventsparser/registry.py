from app import write_json

# ToDo: Chcek for diffrence between id 12,13,14.
def parse_registry_event(event_data):
    """Parse the registry event data and returns a parsed dict"""
    event_time = event_data["UtcTime"]
    event_time = event_time[:event_time.find("."):]
    registry_event = {
    "PID": event_data['ProcessId'],
    "Image": event_data['Image'],
    "TargetObject": event_data['TargetObject'],
    "User": event_data['User'],
    "EventType": event_data['EventType'],
    "UtcTime": event_time
    }
    return registry_event


def registry_events_insertion(registry_events):
    """
    This function recives a list of registry events, 
    parse it and save the output to the DBMS import directory.
    """
    registry = []

    for event in registry_events:
        event_id = event['Event']['System']['EventID']
        event_data = event['Event']['EventData']
        registry.append(parse_registry_event(event_data))

    write_json(registry, "registry")
