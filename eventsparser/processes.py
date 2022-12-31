from app import write_json
import json

def process_events_insertion(process_events):
    # This function receives a list of process events,parse it and save the output to the DBMS import directory.
    pid_list = []
    processes = {}
    # Iterate through process events.
    for event in process_events:
        event_id = event['Event']['System']['EventID']
        event_data = event['Event']['EventData']
        pid = event_data['ProcessId']

        # Process creation.
        if event_id == 1 and pid not in pid_list:
            pid_list.append(pid)
            event_data["Description"] = "Process was created."
            processes[pid] = event_data

        # Termination of a process which its creation was not logged, or not in time range.
        elif event_id == 5 and pid not in pid_list:
            event_data["Description"] = "Process was terminated."
            processes[pid] = event_data

        # Process was created and terminated.
        elif event_id == 5 and pid in pid_list:
            end_time = event_data["UtcTime"]
            end_time = end_time[:end_time.find("."):]
            # find matching process in order to add EndUTCTime and Description.
            processes[pid]["EndUTCTime"] = end_time
            processes[pid]["Description"] = "Process was created and terminated."

    write_json(list(processes.values()), "processes")

