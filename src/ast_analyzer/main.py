"""
ast_analyzer.main

Entry point for the AST Analyzer application
"""

from ast_analyzer.generators.file_traversal import get_working_files


def main():
    # Step 1: Ask user for directory of files
    directory = "./src/ast_analyzer"  # TODO - swap out with CLI command when we get to that story

    # Step 2: Filter out all invalid files from directory
    working_files = get_working_files(directory)

    # Step 3: Start iterating through each file
    for file in working_files:
        print(file)
    # Step 4: Parse through the lines of each file
    # Step 5: Create an AST Node of each file
    # Step 6: Run the nodes through our analysis
    # Step 7: Generate a report based on findings
    print("Hello world")


if __name__ == "__main__":
    main()
