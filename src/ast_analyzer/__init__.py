"""
AST Analyzer: Traverst the syntax tree of a user's project and provide a score or suggestion on how to improve the
quality of the code
"""

import ast


def main():
    print("Hello world!")


class ASTNode:
    """
    Analyze parsed code via AST to generate findings.

    Args:
        tree: The parsed AST tree to analyze

    Attributes:
        tree: The AST being analyzed
        results: Accumulated analysis results
    """

    def __init__(self, node: ast.AST, parent: Optional["ASTNode"] = None) -> None:
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

    def __str__(self):
        return f"AST Node | Children: {len(self)}"

    def __iter__(self):
        """Iterate over children nodes"""
        raise NotImplementedError("ASTANA-5 will implement")

    def __contains__(self, item):
        """checks if node contains an item"""
        raise NotImplementedError("ASTANA-5 will implement")

    def __eq__(self, other):
        """Determine if two nodes are the same"""
        raise NotImplementedError("ASTANA-5 will implement")

    def __hash__(self):
        """Make node hashabloe to be used in sets/dicts"""
        raise NotImplementedError("ASTANA-5 will implement")
