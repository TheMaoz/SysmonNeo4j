import argparse
from datetime import datetime
import json
import webbrowser
from evtx import PyEvtxParser
from app import *


def valid_time(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d-%H:%M:%S")
    except ValueError:
        msg = "not a valid time: {0!r}".format(s)
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
    except Exception as e:
        # TODO: Create a logger
        print(e)
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
    process = {}
    processes = []

    for event in events:
        eventId = event['Event']['System']['EventID']
        if eventId == 1 or eventId == 5:
            pid = event['Event']['EventData']['ProcessId']
            if pid not in pid_list and eventId == 1:
                # create new process
                pid_list.append(pid)
                event_time = event['Event']["EventData"]["UtcTime"]
                event_time = event_time = event_time[:event_time.find("."):]
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
def run(url_db, username, password, directory, neo4jbrowser, graphlytic):
    set_import_path(directory)

    clear_directory()
    # scraper.download_datasets(import_path)
    xml_to_json()
    replace_unwanted_string_cwe()
    replace_unwanted_string_capec()
    copy_files_cypher_script()

    app = App(url_db, username, password)
    app.clear()
    app.close()

    app = App(url_db, username, password)
    app.schema_script()
    app.cve_insertion()
    app.cwe_insertion()
    app.capec_insertion()
    app.cpe_insertion()
    app.close()

    if neo4jbrowser:
        webbrowser.open("http://localhost:7474")
    if graphlytic:
        webbrowser.open("http://localhost:8110/")
    return




def list_to_string(plist):
    """
    :param plist: list of events.
    :return: string of list ready to go into db
    """
    st = '['
    for item in plist:
        st += json.dumps(item) + ','
    st = st[:len(st) - 1] + "]"
    return st



def run_upload_query(plist):
    db_connection = GraphDatabase.driver(uri="bolt://localhost:7687", auth=("neo4j", "password"))
    # :todo: Check connection to db before running any queries using db_connection.verify_connectivity and write to log file.

    session = db_connection.session()
    cleardb_script = open("CypherScripts/ClearDB.cypher").read()
    session.run(cleardb_script, list=list_to_string(plist))
    upload_script = open("CypherScripts/UploadProcess.cypher").read()
    session.run(upload_script, list=list_to_string(plist))
    connect_script = open("CypherScripts/ConnectProcessParent.cypher").read()
    session.run(connect_script)
    # :TODO: add try catch for session.run errors + combine 2 runs into one.


def events_to_db(filename,start,end):
    """
    :desc: FULL PROCEDURE: from evtx to db.
    :TODO: add different types of objects (Processes, Files, RegistryKeys, etc.)
    """
    events = get_json_from_sample(filename)
    events = filter_events_by_time(events, start, end)
    processes = parse_process(events)
    run_upload_query(processes)


def main():
    parser = argparse.ArgumentParser(description='Description of your program')

    parser.add_argument("-s", "--startdate", required=True,
                        help="The Start Time - format YYYY-mm-dd-:HH:MM:SS",
                        type=valid_time
                        )

    parser.add_argument("-e", "--enddate", required=True,
                        help="The End Time format YYYY-mm-dd-:HH:MM:SS",
                        type=valid_time
                        )

    parser.add_argument('-f', '--file', required=True,
                        help='Path to json input file')

    args = parser.parse_args()
    """
    if args.neo4jbrowser == "y" or args.neo4jbrowser == "Y":
        neo4jbrowser_open = True
    else:
        neo4jbrowser_open = False
    if args.graphlytic == "y" or args.neo4jbrowser == "Y":
        graphlytic_open = True
    else:
        graphlytic_open = False
    # run(args.urldb, args.username, args.password,
    # args.directory, neo4jbrowser_open, graphlytic_open)
    """
    events_to_db(filename=args.file,start=args.startdate,end=args.enddate)
    return



if __name__ == "__main__":
    main()

# Command to run:
# .\SysmonNeo4j.py -s 2022-11-22-20:30:05 -e 2022-11-22-20:30:35 -f .\firstsample.evtx
