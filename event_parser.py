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


def parse_process(process_events):
    """
    :desc: takes a list of events and parses it to a list of processes by the following syntax:
    {"processName":"example.exe","Pid":"2123","PPid":"13","StartTime":"","EndTime":""}
    """
    pid_list = []
    processes = []

    for event in process_events:
        eventId = event['Event']['System']['EventID']
        event_data = event['Event']['EventData']
        pid = event_data['ProcessId']
        
        # Process creation.
        if eventId == 1 and pid not in pid_list:
            pid_list.append(pid)
            event_time = event_data["UtcTime"]
            event_time = event_time[:event_time.find("."):]
            image = event_data['Image']
            filename = event_data['OriginalFileName']
            cmd = event_data['CommandLine']
            ppid = event_data['ParentProcessId']
            user = event_data['User']
            process = {
            "PPID": ppid,
            "PID": pid,
            "Image": image,
            "FileName": filename,
            "CommandLine": cmd,
            "Username": user,
            "StartTime": event_time
            }
            processes.append(process)
        
        # End case - to chcek.
        elif eventId == 5 and pid not in pid_list:
            continue
        
        # Process terminate.
        elif eventId == 5 and pid in pid_list:
            end_time = event_data["UtcTime"]
            end_time = end_time[:end_time.find("."):]
            for p in processes:
                if p['PID'] == pid and eventId == 5:
                    p.update({"EndTime": end_time})

    write_json(processes, "processes")

