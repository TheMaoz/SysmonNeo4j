import argparse
from datetime import datetime
import json
import webbrowser
from evtx import PyEvtxParser
from app import *


def valid_time(str_input):
    """validates that the user input time"""
    try:
        return datetime.strptime(str_input, "%Y-%m-%d-%H:%M:%S")
    except ValueError:
        msg = "not a valid time: {0!r}".format(str_input)
        raise argparse.ArgumentTypeError(msg)


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


def parse_process(events):
    """
    :desc: takes a list of events and parses it to a list of processes by the following syntax:
    {"processName":"example.exe","Pid":"2123","PPid":"13","StartTime":"","EndTime":""}
    """
    pid_list = []
    processes = []

    for event in events:
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
    return processes


# Define the functions that will be running
def run(url_db, username, password, directory, file_path, start_time, end_time):
    set_import_path(directory)
    app = App(url_db, username, password)
    clear_directory()
    app.clear()
    app.close()
    events_list = filter_events_by_time(get_json_from_sample(file_path), start_time, end_time)
    process_list = parse_process(events_list)
    write_json(process_list, "processes")
    app = App(url_db, username, password)
    copy_files_cypher_script()
    app.upload_processes()
    app.close()
    return


def main():
    parser = argparse.ArgumentParser(description='Description of your program')

    parser.add_argument("-s", "--starttime", required=True,
                        help="The Start Time - format YYYY-mm-dd-:HH:MM:SS",
                        type=valid_time
                        )

    parser.add_argument("-e", "--endtime", required=True,
                        help="The End Time format YYYY-mm-dd-:HH:MM:SS",
                        type=valid_time
                        )

    parser.add_argument('-l', '--urldb', required=True,
                        help='neo4j url (usually \"bolt://localhost:7687\")')

    parser.add_argument('-f', '--file', required=True,
                        help='Path to Sysmon .evtx file')

    parser.add_argument('-d', '--directory', required=True,
                            help='Path to neo4j DBMS/import directory')

    parser.add_argument('-u', '--username', required=True,
                            help='Neo4j DBMS username')

    parser.add_argument('-p', '--password', required=True,
                            help='Neo4j DBMS password')

    args = parser.parse_args()
    run(args.urldb, args.username, args.password, args.directory, args.file, args.starttime, args.endtime)

    #if args.neo4jbrowser == "y" or args.neo4jbrowser == "Y":
    #    neo4jbrowser_open = True
    #else:
    #    neo4jbrowser_open = False
    #if args.graphlytic == "y" or args.neo4jbrowser == "Y":
    #    graphlytic_open = True
    #else:
    #    graphlytic_open = False
    # run(args.urldb, args.username, args.password,
    # args.directory, neo4jbrowser_open, graphlytic_open)
    return


if __name__ == "__main__":
    main()

# Command to run:
# .\SysmonNeo4j.py -s 2022-11-22-20:30:05 -e 2022-11-22-20:30:35 -f .\firstsample.evtx -p password -u neo4j
# -d "C:\Users\oy703\.Neo4jDesktop\relate-data\dbmss\dbms-df1d6b39-455e-44ef-b1bb-9539850cc4f6\import"
# -l "bolt://localhost:7687"
