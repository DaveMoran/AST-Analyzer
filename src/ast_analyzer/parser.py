"""
ast_analyzer.parser

Traverse the project and transform the data into a readable format for the analzyer to use
"""

import logging


class Parser:
    def __init__(self, filename):
        self.filename = filename
        self.file = None

    def __enter__(self):
        logging.info(f"Begin parsing file {self.filename}")
        self.file = open(self.filename, "r")
        return self.file

    def __exit__(self, exc_type, exc_value, traceback):
        if self.file:
            logging.info(f"File {self.filename} has been fully parsed")
            self.file.close()

        if exc_type:
            print(f"An exception of type {exc_type.__name__} has occured")
        return False


# TODO - Move this to classes/AnalysisResult in follow up chore
class AnalysisResult:
    """
    Takes all of the findings from the CodeAnalyzer class and generates a report
    to share with our user
    """

    def __init__(self):
        self.results = []

    def __repr__(self):
        return f"AnalysisResult(results={self.results})"

    def __str__(self):
        return f"Analysis Complete! There are {len(self)} changes to implement"

    def __len__(self):
        """Return the number of items in the results list"""
        raise NotImplementedError("ASTANA-6 will implement")

    def __bool__(self):
        """Return whether or not theres at least 1 result in the result list"""
        raise NotImplementedError("ASTANA-6 will implement")

    def __getitem__(self, index):
        """Get a specific item from our results list"""
        return self.results[index]

    def __add__(self, other):
        """Combine with results from other scans"""
        raise NotImplementedError("ASTANA-6 will implement")
