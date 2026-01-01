"""
ast_analyzer.parser

Traverse the project and transform the data into a readable format for the analzyer to use
"""


def parser():
    return "parser"


class AnalysisResult:
    """
    Takes all of the findings from the CodeAnalyzer class and generates a report
    to share with our user
    """

    def __init__(self):
        self.results = []

    def __len__(self):
        """Return the number of items in the results list"""

    def __bool__(self):
        """Return whether or not theres at least 1 result in the result list"""

    def __getitem__(self, index):
        """Get a specific item from our results list"""

    def __add__(self, other):
        """Combine with results from other scans"""
