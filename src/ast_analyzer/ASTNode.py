"""
ASTNode Class file
"""

import ast
from typing import Optional


class ASTNode:
    """
    Analyze parsed code via AST to generate findings.

    Args:
        node: The parsed tree to save in our AST Node
        parent: The parent node that the child was generated from

    Attributes:
        tree: The AST being analyzed
        results: Accumulated analysis results
    """

    def __init__(self, node: ast.AST, parent: Optional["ASTNode"] = None) -> None:
        self.node = node
        self.parent = parent
        self.children = []
        self.metadata = {}

        for child in ast.iter_child_nodes(self.node):
            self.children.append(ASTNode(child, self))

    def __repr__(self) -> str:
        return f"ASTNode({type(self.node).__name__})"

    def __len__(self) -> int:
        return len(self.children)

    def __getitem__(self, i: int) -> "ASTNode":
        return self.children[i]

    def __str__(self) -> str:
        return f"AST Node | Children: {len(self)}"

    def __iter__(self):
        for child in self.children:
            yield child

    def __contains__(self, item) -> bool:
        return item in self.children

    def __eq__(self, other) -> bool:
        return self.node == other.node

    def __hash__(self) -> int:
        return hash((self.node, self.parent))
