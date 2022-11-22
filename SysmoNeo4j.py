import argparse


def main():
    print("Maoz")
    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('-f','--foo', help='Description for foo argument', required=True)
    parser.add_argument('-b','--bar', help='Description for bar argument', required=True)
    args = vars(parser.parse_args())

if __name__ == "__main__":
    main()