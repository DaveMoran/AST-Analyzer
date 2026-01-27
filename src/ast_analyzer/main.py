"""
ast_analyzer.main

Entry point for the AST Analyzer application
"""

import argparse
import ast
import logging
import textwrap

from ast_analyzer import ASTNode
from ast_analyzer import analyzer
from ast_analyzer import parser
from ast_analyzer.classes import AnalysisResult
from ast_analyzer.generators import file_traversal


def main():
    # Step 1: Parse CLI arguments for directory
    parser = argparse.ArgumentParser(
        prog="ast-analyzer",
        description="Analyze Python codebases for code quality metrics",
    )
    parser.add_argument(
        "directory",
        help="Path to the directory to analyze",
    )
    parser.add_argument(
        "--show-logs",
        action="store_true",
        help="Show detailed logging output",
    )
    args = parser.parse_args()

    # Configure logging based on flag
    log_level = logging.INFO if args.show_logs else logging.WARNING
    logging.basicConfig(level=log_level)

    directory = args.directory

    # Step 2: Filter out all invalid files from directory
    working_files = file_traversal.get_working_files(directory)
    results = AnalysisResult.AnalysisResult()

    # Step 3: Start iterating through each file
    for file in working_files:
        # Step 4: Parse through the lines of each file
        try:
            with parser.Parser(file) as f:
                # Step 5: Create an AST Node of each file
                content = f.read()
                dedented_code = textwrap.dedent(content)
                test_tree = ast.parse(dedented_code)
                node = ASTNode.ASTNode(test_tree)

                # Step 6: Run the nodes through our analysis
                code_analyzer = analyzer.CodeAnalyzer(node, file, results)

                # Step 7: Generate a report based on findings
                code_analyzer.analyze()

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
