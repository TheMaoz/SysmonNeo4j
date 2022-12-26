import argparse
from datetime import datetime
from app import *
from eventsparser import *
from pathlib import Path

def valid_datetime(str_input):
    """Validates that the user input date time"""
    try:
        return datetime.strptime(str_input, "%Y-%m-%d-%H:%M:%S")
    except ValueError:
        msg = "not a valid time: {0!r}".format(str_input)
        raise argparse.ArgumentTypeError(msg)

def valide_evtx_file(param):
    """Validates the files is an evtx (Windows event log) file"""
    if Path(param).suffix != '.evtx':
        raise argparse.ArgumentTypeError('File must have an evtx extension')
    return param



# Define the functions that will be running
def run(url_db, username, password, file_path, start_time, end_time):
    app = App(url_db, username, password)
    app.set_import_dir()
    #clear_directory()
    app.clear()
    app.close()
    events_list = filter_events_by_time(get_json_from_sample(file_path), start_time, end_time)
    process_events, file_events, registry_events, network_events = divide_events(events_list)
    process_events_insertion(process_events)
    file_events_insertion(file_events)
    registry_events_insertion(registry_events)
    app = App(url_db, username, password)
    app.upload_processes_events()
    app.upload_files_events()
    app.upload_registry_events()
    app.set_nodes_relationship()
    app.close()


def main():
    parser = argparse.ArgumentParser(description='Description of your program')

    parser.add_argument("-s", "--starttime", required=True,
                        help="The Start Time - format YYYY-mm-dd-:HH:MM:SS",
                        type=valid_datetime
                        )

    parser.add_argument("-e", "--endtime", required=True,
                        help="The End Time format YYYY-mm-dd-:HH:MM:SS",
                        type=valid_datetime
                        )

    parser.add_argument('-l', '--urldb', required=False,
                        default="bolt://localhost:7687",
                        help='neo4j url - (usually \"bolt://localhost:7687\")')

    parser.add_argument('-f', '--file', required=True,
                        help='Path to Sysmon .evtx file',
                        type=valide_evtx_file)

    parser.add_argument('-u', '--username', required=True,
                        help='Neo4j DBMS username')

    parser.add_argument('-p', '--password', required=True,
                        help='Neo4j DBMS password')
    args = parser.parse_args()

    run(args.urldb, args.username, args.password,
        args.file, args.starttime, args.endtime)
    return


if __name__ == "__main__":
    main()

# Command to run:
# .\SysmonNeo4j.py -s 2022-11-22-20:30:05 -e 2022-11-22-20:30:35 -f .\evtx_samples\firstsample.evtx -p password -u neo4j
