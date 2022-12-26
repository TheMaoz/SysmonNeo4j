import json

from app import write_json
def file_events_insertion(file_events):
    """
    This function receives a list of file events,
    parse it and save the output to the DBMS import directory.
    """
    pid_list = []
    files = []
    for event in file_events:
        # ToDo: Check for difference between id 11,23.
        event_id = event['Event']['System']['EventID']
        event_data = event['Event']['EventData']
        pid = event_data['ProcessId']
        # File creation.
        if event_id == 11 and pid not in pid_list:
            pid_list.append(pid)
            files.append(event_data)
        # File deletion of a file which its creation was not logged, or not in time range.
        elif event_id == 23 and pid not in pid_list:
            event_data.update({"Description": "File was deleted."})
            files.append(event_data)
        # File was created and deleted.
        elif event_id == 23 and pid in pid_list:
            end_time = event_data["UtcTime"]
            end_time = end_time[:end_time.find("."):]
            for file in files:
                if file['ProcessId'] == pid:
                    file.update({"EndUTCTime": end_time})
                    file.update({"Description": "File was created and deleted."})
        # Only CreateFile was logged.
        for file in files:
            if not ('EndUTCTime' in file):
                file.update({"Description": "File was created."})
    write_json(files, "files")
