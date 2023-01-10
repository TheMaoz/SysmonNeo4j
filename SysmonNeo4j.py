import argparse
from pathlib import Path
from datetime import datetime
from app import App,clear_import_directory
from eventsparser.general import *

SYSMON_EVENT_IDS = {
        "process" : [1,5],
        "file" : [11,23,26],
        "registry" : [12,13,14],
        "network" : [3],
    }


def valid_datetime(str_input):
    """Validates that the user input is a datetime string"""
    try:
        return datetime.strptime(str_input, "%Y-%m-%d-%H:%M:%S")
    except ValueError:
        msg = f"not a valid time: {str_input}"
        raise argparse.ArgumentTypeError(msg)

def valid_evtx_file(param):
    """Validates the file has an evtx (Windows event log) extension"""
    if Path(param).suffix != '.evtx':
        raise argparse.ArgumentTypeError('File must have an evtx extension')
    return param


def run(url_db, username, password, file_path, start_time, end_time):
    app = App(url_db, username, password)
    app.set_import_dir()
    clear_import_directory()
    app.clear()
    app.close()
    
    # Time range args has not been set.
    if None in (start_time, end_time):
        print("\nTime range arguments has not been set.")
        print(f"\nScanning the entire {Path(file_path).name} sample.")
        events_list = get_json_from_sample(file_path)
    else:
        print(f"\nScanning the {Path(file_path).name} sample between: {start_time} - {end_time}.")
        events_list = filter_events_by_time(get_json_from_sample(file_path), start_time, end_time)
    
    insert_sysmon_events(events_list, SYSMON_EVENT_IDS)
    app = App(url_db, username, password)
    app.upload_processes_events()
    app.upload_files_events()
    app.upload_registry_events()
    app.upload_network_events()
    app.set_nodes_relationship()
    app.close()


def main():
    parser = argparse.ArgumentParser(description='Description of your program')

    parser.add_argument("-s", "--starttime", required=False,
                        help="The Start Time - format YYYY-mm-dd-:HH:MM:SS",
                        type=valid_datetime
                        )

    parser.add_argument("-e", "--endtime", required=False,
                        help="The End Time format YYYY-mm-dd-:HH:MM:SS",
                        type=valid_datetime
                        )

    parser.add_argument('-l', '--urldb', required=False,
                        default="bolt://localhost:7687",
                        help='neo4j url - set to \"bolt://localhost:7687\" by default')

    parser.add_argument('-f', '--file', required=True,
                        help='Path to Sysmon .evtx file',
                        type=valid_evtx_file)

    parser.add_argument('-u', '--username', required=False,
                        default="neo4j", help='Neo4j DBMS username,'
                                              ' set to \'neo4j\' by default')

    parser.add_argument('-p', '--password', required=False,
                        default="password", help='Neo4j DBMS password'
                                                 ' set to \'password\' by default')
    args = parser.parse_args()

    run(args.urldb, args.username, args.password,
        args.file, args.starttime, args.endtime)
    return


if __name__ == "__main__":
    main()
