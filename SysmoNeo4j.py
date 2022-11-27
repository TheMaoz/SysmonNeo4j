import argparse
from datetime import datetime
import json
import webbrowser
from evtx import PyEvtxParser
from app import App

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

<<<<<<< HEAD

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


def select_event_fields(events):
    """
    :desc: This function chooses fields for each event specified in 'fields.yml' file.
    :return: a list of events ready to enter db
    TODO: connect processes by events 1&5 with identical PID's.
  
    logs = {}
    log = {}
    fields = []
    with open("fields.yml", 'r') as file:
        yml_fields = yaml.safe_load(file)["fields"]
        for item in yml_fields:
            fields.append(item)
    for event in events:
        for field in fields:
            # print(event['Event'])
            p = tuple(field['path'].split('/'))
            for i in range(len(p)):
                v = event[p[i]]
        Still a work in progress...
    """





=======
>>>>>>> 21a6cfab24d2015ada1cfe964122f1f4f02305b5
# Define the functions that will be running
def run(url_db, username, password, directory, neo4jbrowser, graphlytic):
    set_import_path(directory)

    clear_directory()
    scraper.download_datasets(import_path)
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

    parser.add_argument('-f','--file', required=True,
    help='Path to json input file')

    args = parser.parse_args()
    if args.neo4jbrowser == "y" or args.neo4jbrowser == "Y":
        neo4jbrowser_open = True
    else:
        neo4jbrowser_open = False
    if args.graphlytic == "y" or args.neo4jbrowser == "Y":
        graphlytic_open = True
    else:
        graphlytic_open = False
    #run(args.urldb, args.username, args.password,
        #args.directory, neo4jbrowser_open, graphlytic_open)
    return

if __name__ == "__main__":
    main()
