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
    event_ids = {
        "process" : (1,5),
        "file" : (11,23)
    }
    process_events = []
    file_events = []
    
    # Append events to relavent list.
    for event in events:
        event_id = event['Event']['System']['EventID']
        if event_id in event_ids['process']:
            process_events.append(event)
        elif event_id in event_ids['file']:
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
        if eventId == 1 or eventId == 5:
            pid = event['Event']['EventData']['ProcessId']
            if pid not in pid_list and eventId == 1:
                # create new process
                pid_list.append(pid)
                event_time = event['Event']["EventData"]["UtcTime"]
                event_time = event_time[:event_time.find("."):]
                image = event['Event']['EventData']['Image']
                filename = event['Event']['EventData']['OriginalFileName']
                cmd = event['Event']['EventData']['CommandLine']
                ppid = event['Event']['EventData']['ParentProcessId']
                user = event['Event']['EventData']['User']
            elif pid not in pid_list and eventId == 5:
                continue
            process = {
                "PPID": ppid,
                "PID": pid,
                "Image": image,
                "FileName": filename,
                "CommandLine": cmd,
                "Username": user,
                "StartTime": event_time
                # starttime stays last to stay close to endtime
            }
            processes.append(process)
            if pid in pid_list and eventId == 5:
                end_time = event['Event']["EventData"]["UtcTime"]
                end_time = end_time[:end_time.find("."):]
                for p in processes:
                    if p['PID'] == pid and eventId == 5:
                        p.update({"EndTime": end_time})
    write_json(processes, "processes")

