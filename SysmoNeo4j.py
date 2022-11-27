import argparse
import datetime
import json
from evtx import PyEvtxParser

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

def main():
    parser = argparse.ArgumentParser(description='Description of your program')
    
    parser.add_argument(
    "-s", 
    "--startdate", 
    help="The Start Time - format YYYY-mm-dd-:HH:MM:SS", 
    required=True, 
    type=valid_time
    )

    parser.add_argument(
    "-e", 
    "--enddate", 
    help="The End Time format YYYY-mm-dd-:HH:MM:SS", 
    required=True, 
    type=valid_time
    )

    parser.add_argument('-f','--file', help='Path to json input file', required=True)
    args = vars(parser.parse_args())

if __name__ == "__main__":
    main()
