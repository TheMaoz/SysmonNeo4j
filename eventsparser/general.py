import json
from datetime import datetime
from evtx import PyEvtxParser

def get_json_from_sample(sample):
    """
    :desc: This function gets sysmon sample of type evtx and returns a list of sysmon events
    sample: evtx file sample
    event_list → list of sysmon events
    """
    event_list = []
    try:
        parser = PyEvtxParser(sample)
        for record in parser.records_json():
            event_list.append(json.loads(record['data']))
    except Exception as error:
        print(error)
        return None
    return event_list


def filter_events_by_time(events, start_time, end_time):
    """
    :desc: This function sorts list by time, then filters said list by time range specified by user.
    events: list to sort and filter.
    start_time & end_time: specified by user in CLI.
    logs → sorted and filtered list.
    """
    logs = []
    events.sort(key=lambda x: x['Event']["System"]["TimeCreated"]["#attributes"]["SystemTime"])
    for event in events:
        event_time = event['Event']["System"]["TimeCreated"]["#attributes"]["SystemTime"]
        event_time = event_time[:event_time.find("."):]
        event_time = datetime.strptime(event_time, "%Y-%m-%dT%H:%M:%S")
        if start_time <= event_time <= end_time:
            logs.append(event)
    return logs


def divide_events(events):
    """
    Takes a list of events and returns lists of events group by object types.
    """
    process_events = []
    file_events = []
    registry_events = []
    network_events = []
    
    # Append events to relevant list.
    for event in events:
        event_id = event['Event']['System']['EventID']
        
        # Process events.
        if event_id in (1, 5):
            process_events.append(event)
        
        # File events.
        elif event_id in (11, 23):
            file_events.append(event)
        
        # Registry events.
        elif event_id in (12,13,14):
            registry_events.append(event)
        
        # Network events.
        elif event_id == 3:
            network_events.append(event)
    return process_events, file_events, registry_events, network_events
    