from app import write_json

def file_events_insertion(file_events):
    """
    :desc This function receives a list of file events,
    aggregate file events in dictionary keys, if Image[PID] -> TargetFilename are the same.
    Stores a description about the file operations under 'Description' key.
    If a file was created and deleted by the same process stores deletion time under "EndUTCTime".
    Saves the output to the DBMS import directory.
    file_events: list of Sysmon file events(11, 23, 26).
    """
    file_ids = []
    files = {}
    

    # Iterate through file events.
    for event in file_events:
        event_id = event['Event']['System']['EventID']
        event_data = event['Event']['EventData']
        image = event_data['Image']
        pid = event_data['ProcessId']
        target_file = event_data['TargetFilename']
        
        file_id = f"{image}[{pid}]->{target_file}"
        
        # File creation.
        if event_id == 11:
            file_ids.append(file_id)
            event_data["Description"] = "File was created."
            files[file_id] = event_data
        
        # File was created and deleted.
        elif event_id in (23,26) and file_id in file_ids:
            end_time = event_data["UtcTime"]
            end_time = end_time[:end_time.find("."):]
            files[file_id]["EndUTCTime"] = end_time
            files[file_id]["Description"] = "File was created and deleted."

        # File deletion of a file which its creation was not logged, or not in time range.
        elif event_id in (23,26) and file_id not in file_ids:
            file_ids.append(file_id)
            event_data["Description"] = "File was deleted."
            files[file_id] = event_data
    write_json(list(files.values()), "files")
