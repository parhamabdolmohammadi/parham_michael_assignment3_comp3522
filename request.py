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

        self.mode = None
        self.input_data = None
        self.expanded = False
        self.output_file = None
        self.isFromFile = False

    def __str__(self):
        """
        Returns a string representation of the Request object.

        Returns:
            str: A formatted string showing the current request's attributes.
        """

        return (
            f"Mode: {self.mode}\n"
            f"Input Data: {self.input_data}\n"
            f"Expanded: {self.expanded}\n"
            f"Output File: {self.output_file}\n"
            f"Is From File: {self.isFromFile}"
        )
