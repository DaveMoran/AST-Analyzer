"""
ast_analyzer.main

Entry point for the AST Analyzer application
"""

import ast
import logging
import textwrap

from ast_analyzer.ASTNode import ASTNode
from ast_analyzer.generators.file_traversal import get_working_files
from ast_analyzer.parser import Parser

logging.basicConfig(level=logging.INFO)


def main():
    # Step 1: Ask user for directory of files
    directory = "./src/ast_analyzer"  # TODO - swap out with CLI command when we get to that story

    # Step 2: Filter out all invalid files from directory
    working_files = get_working_files(directory)

    # Step 3: Start iterating through each file
    for file in working_files:
        # Step 4: Parse through the lines of each file
        try:
            with Parser(file) as f:
                # Step 5: Create an AST Node of each file
                content = f.read()
                dedented_code = textwrap.dedent(content)
                test_tree = ast.parse(dedented_code)
                node = ASTNode(test_tree)

        except FileNotFoundError:
            logging.exception(f"File not found: {file}")

        except SyntaxError:
            logging.exception(f"{file} contains a Syntax error")

        except UnicodeDecodeError:
            logging.exception(f"{file} contains encoding issues")

    # Step 6: Run the nodes through our analysis - ASTANA-6
    # Step 7: Generate a report based on findings - ASTANA-11
    print("Hello world")


if __name__ == "__main__":
    main()
