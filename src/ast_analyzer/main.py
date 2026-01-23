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
from ast_analyzer.analyzer import CodeAnalyzer
from ast_analyzer.classes.AnalysisResult import AnalysisResult

logging.basicConfig(level=logging.INFO)


def main():
    # Step 1: Ask user for directory of files
    directory = "./src/ast_analyzer"  # TODO - swap out with CLI command when we get to that story

    # Step 2: Filter out all invalid files from directory
    working_files = get_working_files(directory)
    results = AnalysisResult()

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

                # Step 6: Run the nodes through our analysis
                analyzer = CodeAnalyzer(node, file, results)

                # Step 7: Generate a report based on findings
                new_result = analyzer.analyze()
                results += new_result

        except FileNotFoundError:
            logging.exception(f"File not found: {file}")

        except SyntaxError:
            logging.exception(f"{file} contains a Syntax error")

        except UnicodeDecodeError:
            logging.exception(f"{file} contains encoding issues")

    # Step 8: Print results to user
    print(results)


if __name__ == "__main__":
    main()
