"""
ASTNode Class file
"""

import ast
from typing import Optional


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
        return self.children

    def __contains__(self, item):
        return item in self.children

    def __eq__(self, other):
        return self.node == other.node

    def __hash__(self):
        return hash(self.node, self.parent, self.children, self.metadata)
