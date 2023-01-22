import json
from datetime import datetime
from evtx import PyEvtxParser
from .processes import process_events_insertion
from .files import file_events_insertion
from .registry import registry_events_insertion
from .network import network_events_insertion
from .sysmon_config_events import config_events_insertion

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


def insert_sysmon_events(events, event_ids):
    """
    :desc This function gets a list of sysmon events,
    divide them by object type ids and insert them into the DBMS import dir.
    :events List of Sysmon events(json).
    :event_ids: Dictionary of Sysmon event id values by object keys.
    """
    
    # Creating lists of events group by object type.
    process_events = [event for event in events if event['Event']['System']['EventID'] in event_ids['process']]
    file_events = [event for event in events if event['Event']['System']['EventID'] in event_ids['file']]
    registry_events = [event for event in events if event['Event']['System']['EventID'] in event_ids['registry']]
    network_events = [event for event in events if event['Event']['System']['EventID'] in event_ids['network']]
    sysmon_config_events = [event for event in events if event['Event']['System']['EventID'] in event_ids['config']]

    # Inserting data to the DBMS import directory.
    process_events_insertion(process_events)
    file_events_insertion(file_events)
    registry_events_insertion(registry_events)
    network_events_insertion(network_events)
    config_events_insertion(sysmon_config_events)