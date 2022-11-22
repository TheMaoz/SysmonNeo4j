import argparse
import datetime

def valid_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d-%H:%M:%S")
    except ValueError:
        msg = "not a valid date: {0!r}".format(s)
        raise argparse.ArgumentTypeError(msg)

def main():
    parser = argparse.ArgumentParser(description='Description of your program')
    
    parser.add_argument(
    "-s", 
    "--startdate", 
    help="The Start Time - format YYYY-mm-dd-:HH:MM:SS", 
    required=True, 
    type=valid_date
    )

    parser.add_argument(
    "-e", 
    "--enddate", 
    help="The End Time format YYYY-mm-dd-:HH:MM:SS (Inclusive)", 
    required=True, 
    type=valid_date
    )

    parser.add_argument('-f','--file', help='Path to json input file', required=True)
    args = vars(parser.parse_args())

if __name__ == "__main__":
    main()