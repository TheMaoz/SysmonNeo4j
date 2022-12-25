from app import write_json

# ToDo: Chcek for diffrence between id 11,23.
def parse_file_event(event_data):
    """Parse the file event data and returns a parsed dict"""
    event_time = event_data["UtcTime"]
    event_time = event_time[:event_time.find("."):]
    file_event = {
    "PID": event_data['ProcessId'],
    "Image": event_data['Image'],
    "TargetFilename": event_data['TargetFilename'],
    "CreationUtcTime": event_data['CreationUtcTime'],
    "User": event_data['User'],
    "UtcTime": event_time
    }
    return file_event


def file_events_insertion(file_events):
    """
    This function recives a list of file events, 
    parse it and save the output to the DBMS import directory.
    """
    files = []

    for event in file_events:
        event_id = event['Event']['System']['EventID']
        event_data = event['Event']['EventData']
        files.append(parse_file_event(event_data))

    write_json(files, "files")
