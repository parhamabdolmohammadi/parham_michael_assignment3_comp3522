# Name: Michael McBride
# Student number: A01394787
# Name: Parham Abdolmohammadi
# Student number: A01356970


import argparse
import asyncio
import time

from request import Request
from retrieverFacade import PokedexRetrieverFacade


def setup_request_commandline() -> Request | list[Request]:
    """
    Parses command-line arguments to configure and return one or more Request objects.

    Returns:
        Request | list[Request]: A single or list of Request objects based on user input.

    Exits:
        The program exits with an error message if required arguments are missing
        or if the input file format is invalid.
    """

    parser = argparse.ArgumentParser()

    parser.add_argument("mode", choices=["pokemon", "ability", "move"])

    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument("--inputfile", help="Text file containing input data (e.g., names or ids)")
    group.add_argument("--inputdata", help="Single name or id input")

    parser.add_argument("--expanded", action="store_true", help="Enable expanded mode")

    parser.add_argument("--output", help="Optional output file to write results")

    try:
        args = parser.parse_args()


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
            new_request = Request()
            new_request.mode = args.mode
            new_request.input_file = args.inputfile
            new_request.input_data = args.inputdata
            new_request.expanded = args.expanded
            new_request.output_file = args.output
            new_request.isFromFile = False

            requests.append(new_request)

        else:

            with open(args.inputfile, "r") as input_file:
                for line in input_file:
                    line = line.strip()

                    if line != "":
                        new_request = Request()
                        new_request.mode = args.mode
                        new_request.input_data = line
                        new_request.expanded = args.expanded
                        new_request.output_file = args.output
                        new_request.isFromFile = False
                        requests.append(new_request)

        return requests

    except Exception as e:
        print(f"Error! Could not read arguments.\n{e}")
        quit()


def output_data(file_name, pokedex):
    """
    Outputs Pokédex data to the console or writes it to a file.

    Args:
        file_name (str | None): The name of the output file, or None for console output.
        pokedex (list): A list of PokedexObject instances to output.
    """

    if file_name is None:
        [print(pokedex_object) for pokedex_object in pokedex]
    else:
        try:
            with open(file_name, "a+") as output_file:
                output_file.write(f"Timestamp: {time.strftime('%d/%m/%Y %H:%M')}\n")
                output_file.write(f"Number of requests: {len(pokedex)}\n\n")
                [output_file.write(str(pokedex_object)) for pokedex_object in pokedex]
        except IOError:
            print(f"Error encountered writing to {file_name}")
        else:
            print(f"Request processed. Please see {file_name}")


async def main(requests: list[Request]):
    """
    Asynchronously executes the given requests using the PokedexRetrieverFacade.

    Args:
        requests (list[Request]): A list of Request objects to process.

    Returns:
        list: A list of PokedexObject instances returned by the retriever.
    """

    retrieve_facade = PokedexRetrieverFacade()
    return await retrieve_facade.execute_request(requests)


if __name__ == '__main__':
    request = setup_request_commandline()
    pokedex_data = asyncio.run(main(request))
    output_data(request[0].output_file, pokedex_data)
