from app import write_json

def process_events_insertion(process_events):
    '''
    :desc This function receives a list of process events,
    aggregate process events in dictionary keys, if Image[PID] are the same.
    Stores the UTC times a process was terminated under 'EndUTCTime' key.
    Saves the output to the DBMS import directory.
    process_events: list of Sysmon process events(1 & 5).
    '''
    process_ids = []
    processes = {}

    # Iterate through process events.
    for event in process_events:
        event_id = event['Event']['System']['EventID']
        event_data = event['Event']['EventData']
        image = event_data['Image']
        pid = event_data['ProcessId']
        process_id = f"{image}[{pid}]"

        # Process creation.
        if event_id == 1 and process_id not in process_ids:
            process_ids.append(process_id)
            event_data["Description"] = "Process was created."
            processes[process_id] = event_data

        # Process was created and terminated.
        elif event_id == 5 and process_id in process_ids:
            end_time = event_data["UtcTime"]
            end_time = end_time[:end_time.find("."):]
            # find matching process in order to add EndUTCTime and Description.
            processes[process_id]["EndUTCTime"] = end_time
            processes[process_id]["Description"] = "Process was created and terminated."

        # Termination of a process which its creation was not logged, or not in time range.
        elif event_id == 5 and process_id not in process_ids:
            process_ids.append(process_id)
            event_data["Description"] = "Process was terminated."
            processes[process_id] = event_data
        
        
    write_json(list(processes.values()), "processes")

