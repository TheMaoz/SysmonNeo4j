import argparse
import webbrowser
from app import *
from event_parser import *

def valid_datetime(str_input):
    """validates that the user input datetime"""
    try:
        return datetime.strptime(str_input, "%Y-%m-%d-%H:%M:%S")
    except ValueError:
        msg = "not a valid time: {0!r}".format(str_input)
        raise argparse.ArgumentTypeError(msg)



# Define the functions that will be running
def run(url_db, username, password, directory, file_path, start_time, end_time):
    set_import_path(directory)
    app = App(url_db, username, password)
    clear_directory()
    app.clear()
    app.close()
    events_list = filter_events_by_time(get_json_from_sample(file_path), start_time, end_time)
    process_events, file_events = divide_events(events_list)
    parse_process(process_events)
    app = App(url_db, username, password)
    copy_files_cypher_script()
    app.upload_processes()
    app.close()
    return


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
