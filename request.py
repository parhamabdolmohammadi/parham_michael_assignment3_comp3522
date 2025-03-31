# Name: Michael McBride
# Student number: A01394787
# Name: Parham Abdolmohammadi
# Student number: A01356970

class Request:
    """
    Represents a single request for Pokédex data retrieval.
    Holds information about the type of data requested, input identifier,
    whether expanded data is needed, and output configuration.
    """

    def __init__(self):
        """
        Initializes a new Request object with default values.
        """

        self.__mode = None
        self.__input_data = None
        self.__expanded = False
        self.__output_file = None
        self.__is_from_file = False

    def get_mode(self):
        """
        Returns the mode of the request.

        Returns:
            str: The mode of the request.
        """
        return self.__mode

    def get_input_data(self):
        """
        Returns the input data for the request.

        Returns:
            str: The input identifier (e.g., name or ID).
        """
        return self.__input_data

    def get_expanded(self):
        """
        Returns whether expanded data is requested.

        Returns:
            bool: True if expanded data is requested, False otherwise.
        """
        return self.__expanded

    def get_output_file(self):
        """
        Returns the output file path for the request.

        Returns:
            str: The output file path or None if not specified.
        """
        return self.__output_file

    def is_from_file(self):
        """
        Returns whether the input data was sourced from a file.

        Returns:
            bool: True if input data is from a file, False otherwise.
        """
        return self.__is_from_file

    def set_mode(self, mode):
        """
        Sets the mode of the request.

        Args:
            mode (str): The type of data being requested (e.g., 'pokemon', 'move').
        """
        self.__mode = mode

    def set_input_data(self, input_data):
        """
        Sets the input data identifier for the request.

        Args:
            input_data (str): The name or ID of the data being requested.
        """
        self.__input_data = input_data

    def set_expanded(self, expanded):
        """
        Sets whether expanded information should be retrieved.

        Args:
            expanded (bool): True to retrieve expanded data, False otherwise.
        """
        self.__expanded = expanded

    def set_output_file(self, output_file):
        """
        Sets the output file path for storing the response.

        Args:
            output_file (str): The path to the file where output will be saved.
        """
        self.__output_file = output_file

    def set_is_from_file(self, is_from_file):
        """
        Sets whether the input data is sourced from a file.

        Args:
            is_from_file (bool): True if input is from a file, False otherwise.
        """
        self.__isfromFile = is_from_file

    def __str__(self):
        """
        Returns a string representation of the Request object.

        Returns:
            str: A formatted string showing the current request's attributes.
        """

        return (
            f"Mode: {self.__mode}\n"
            f"Input Data: {self.__input_data}\n"
            f"Expanded: {self.__expanded}\n"
            f"Output File: {self.__output_file}\n"
            f"Is From File: {self.__isFromFile}"
        )
