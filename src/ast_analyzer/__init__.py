"""
AST Analyzer: Traverst the syntax tree of a user's project and provide a score or suggestion on how to improve the
quality of the code
"""

import ast


def main():
    print("Hello world!")


def ASTNode():
    """Wrapper around ast nodes with analysis metadata."""

    def __init__(self, node: ast.AST, parent):
        self.node = node
        self.parent = parent
        self.children = []
        self.metadata = {}

    def __repr__(self):
        return f"ASTNode({type(self.node).__name__})"

    def __len__(self):
        return len(self.children)

    def __getitem__(self, i):
        return self.children[i]

    def __iter__(self):
        """Iterate over children nodes"""
        return

    def __contains__(self, item):
        """checks if node contains an item"""
        return

    def __str__(self):
        return f"AST Node | Children: {len(self)}"

    def __eq__(self, other):
        """Determine if two nodes are the same"""

    def __hash__(self):
        """Make node hashaboe to be used in sets/dicts"""
