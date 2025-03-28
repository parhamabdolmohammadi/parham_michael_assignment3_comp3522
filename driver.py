# Name:
# Student number:
import argparse

import requests

from request import Request


def setup_request_commandline() -> Request | list[Request]:
    parser = argparse.ArgumentParser()

    parser.add_argument("mode", choices=["pokemon", "ability", "move"])

    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument("--inputfile", help="Text file containing input data (e.g., names or ids)")
    group.add_argument("--inputdata", help="Single name or id input")

    parser.add_argument("--expanded", action="store_true", help="Enable expanded mode")

    parser.add_argument("--output", help="Optional output file to write results")

    try:
        args = parser.parse_args()

        # Manual mutual exclusivity check for custom message
        if args.inputfile and args.inputdata:
            print("Error: You cannot provide both --inputfile and --inputdata at the same time.")
            quit()
        elif not args.inputfile and not args.inputdata:
            print("Error: You must provide either --inputfile or --inputdata.")
            quit()

        if args.inputfile:
            splitted = args.inputfile.split(".")
            if splitted[-1] != "txt":
                print("Error: file extension must be in txt format.")
                quit()


        requests = []


        if args.inputdata:
            request = Request()
            request.mode = args.mode
            request.input_file = args.inputfile
            request.input_data = args.inputdata
            request.expanded = args.expanded
            request.output_file = args.output
            request.isFromFile = False

            requests.append(request)

        else:

            with open(args.inputfile, "r") as input_file:
                for line in input_file:
                    line = line.strip()

                    if line != "":
                        request = Request()
                        request.mode = args.mode
                        request.input_data = line
                        request.expanded = args.expanded
                        request.output_file = args.output
                        request.isFromFile = False
                        requests.append(request)


        return requests

    except Exception as e:
        print(f"Error! Could not read arguments.\n{e}")
        quit()



def main(requests: list[Request]):
    for request in requests:
        print(request)
        print("")


if __name__ == '__main__':
    request = setup_request_commandline()
    main(request)
