import argparse
from datetime import datetime
from app import *
from eventsparser import *


def valid_datetime(str_input):
    """validates that the user input datetime"""
    try:
        return datetime.strptime(str_input, "%Y-%m-%d-%H:%M:%S")
    except ValueError:
        msg = "not a valid time: {0!r}".format(str_input)
        raise argparse.ArgumentTypeError(msg)


# Define the functions that will be running
def run(url_db, username, password, file_path, start_time, end_time):
    app = App(url_db, username, password)
    clear_directory()
    app.clear()
    app.close()
    events_list = filter_events_by_time(get_json_from_sample(file_path), start_time, end_time)
    process_events, file_events = divide_events(events_list)
    process_insertion(process_events)
    app = App(url_db, username, password)
    app.upload_processes()
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

    parser.add_argument('-l', '--urldb', required=True,
                        help='neo4j url (usually \"bolt://localhost:7687\")')

    parser.add_argument('-f', '--file', required=True,
                        help='Path to Sysmon .evtx file')

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
# .\SysmonNeo4j.py -s 2022-11-22-20:30:05 -e 2022-11-22-20:30:35 -f .\firstsample.evtx -p password -u neo4j -l "bolt://localhost:7687"
