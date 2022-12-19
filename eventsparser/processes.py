from app import write_json

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
            for process in processes:
                if process['PID'] == pid:
                    process.update({"EndTime": end_time})

    write_json(processes, "processes")
