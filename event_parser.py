from evtx import PyEvtxParser
from datetime import datetime
import json
from app import write_json


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
        # TODO: Create a logger
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
    
    # Append events to relavent list.
    for event in events:
        event_id = event['Event']['System']['EventID']
        
        # Process events.
        if event_id in (1,5):
            process_events.append(event)
        
        # File events.
        elif event_id in (11,23):
            file_events.append(event)
    
    return process_events,file_events

def parse_process_event(event_data):
    """Parse the process event data and returns a parsed dict"""
    event_time = event_data["UtcTime"]
    event_time = event_time[:event_time.find("."):]
    process_event = {
    "PPID": event_data['ParentProcessId'],
    "PID": event_data['ProcessId'],
    "Image": event_data['Image'],
    "FileName": event_data['OriginalFileName'],
    "CommandLine": event_data['CommandLine'],
    "Username": event_data['User'],
    "StartTime": event_time
    }

    return process_event


def process_insertion(process_events):
    """
    :desc: takes a list of events and parses it to a list of processes by the following syntax:
    {"processName":"example.exe","Pid":"2123","PPid":"13","StartTime":"","EndTime":""}
    """
    pid_list = []
    processes = []

    for event in process_events:
        event_id = event['Event']['System']['EventID']
        event_data = event['Event']['EventData']
        pid = event_data['ProcessId']
        
        # Process creation.
        if event_id == 1 and pid not in pid_list:
            pid_list.append(pid)
            processes.append(parse_process_event(event_data))
        
        # End case - to chcek.
        elif event_id == 5 and pid not in pid_list:
            continue
        
        # Process terminate.
        elif event_id == 5 and pid in pid_list:
            end_time = event_data["UtcTime"]
            end_time = end_time[:end_time.find("."):]
            for p in processes:
                if p['PID'] == pid:
                    p.update({"EndTime": end_time})

    write_json(processes, "processes")

