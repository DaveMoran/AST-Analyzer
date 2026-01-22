"""
ast_analyzer.parser

Traverse the project and transform the data into a readable format for the analzyer to use
"""

import logging


class Parser:
    """Context manager for the AST Node parser to handle individual files

    Args:
        filename: Name of the file that you'll be parsing

    Example:
        >>> file_parser = Parser('./src/ast_analyzer/parser.py')
    """

    def __init__(self, filename: str):
        self.filename = filename
        self.file = None

    def __enter__(self):
        if self.file is not None and self.file.closed:
            raise ValueError("Cannot reuse Parser instance after file is closed")
        logging.info(f"Begin parsing file {self.filename}")
        self.file = open(self.filename, "r")
        return self.file

    def __exit__(self, exc_type, exc_value, traceback):
        if self.file:
            logging.info(f"File {self.filename} has been fully parsed")
            self.file.close()

        if exc_type:
            logging.error(
                f"Exception when trying to parse {self.filename}:",
                exc_info=(exc_type, exc_value, traceback),
            )
        return False
