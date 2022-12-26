from app import write_json




def process_events_insertion(process_events):
    """
    This function recives a list of process events,
    parse it and save the output to the DBMS import directory.
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
            processes.append(event_data)
        # Termination of a process which its creation was not logged, or not in time range.
        elif event_id == 5 and pid not in pid_list:
            event_data.update({"Description": "Process was terminated."})
            processes.append(event_data)
        # Process terminate.
        elif event_id == 5 and pid in pid_list:
            end_time = event_data["UtcTime"]
            end_time = end_time[:end_time.find("."):]
            for process in processes:
                if process['ProcessId'] == pid:
                    process.update({"EndUTCTime": end_time})
                    process.update({"Description": "Process was created and terminated."})
        # Only CreateProcess was logged.
        for process in processes:
            if not('EndTime' in process):
                process.update({"Description": "Process was created."})
    write_json(processes, "processes")
