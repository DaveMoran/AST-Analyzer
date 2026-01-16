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
        # self.metadata = {} TODO - Check if this is used for later imnplementation

        for child in ast.iter_child_nodes(self.node):
            self.children.append(ASTNode(child, self))

    def __repr__(self) -> str:
        """Dev-friendly string for debugging purposes"""
        return f"ASTNode({type(self.node).__name__})"

    def __len__(self) -> int:
        """Return the length of children for this node"""
        return len(self.children)

    def __getitem__(self, i: int) -> "ASTNode":
        """Return a specific child from this node"""
        return self.children[i]

    def __str__(self) -> str:
        """A user-friendly string representation showing details of the node"""
        return f"AST Node | Children: {len(self)}"

    def __iter__(self):
        """Iterate through the children of this node"""
        for child in self.children:
            yield child

    def __contains__(self, item) -> bool:
        """Check if the node contains a specific child"""
        return item in self.children

    def __eq__(self, other) -> bool:
        """Check if this node is identical to another"""
        return self.node == other.node

    def __hash__(self) -> int:
        """Returns a hash value that represents the node"""
        return hash((self.node, self.parent))
