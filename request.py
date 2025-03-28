class Request:
    def __init__(self):
        self.mode = None
        self.input_file = None
        self.input_data = None
        self.expanded = False
        self.output_file = None

    def __str__(self):
        return (
            f"Mode: {self.mode}\n"
            f"Input File: {self.input_file}\n"
            f"Input Data: {self.input_data}\n"
            f"Expanded: {self.expanded}\n"
            f"Output File: {self.output_file}"
        )
