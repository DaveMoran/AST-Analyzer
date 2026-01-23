"""
ASTNode Class file
"""

import ast
from typing import Optional, Any


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
        self.has_docstring = False
        if type(node).__name__ in [
            "FunctionDef",
            "AsyncFunctionDef",
            "ClassDef",
            "Module",
        ] and ast.get_docstring(node):
            self.has_docstring = True

        # Calculate line count if both lineno and end_lineno exist
        start_line = getattr(node, "lineno", None)
        end_line = getattr(node, "end_lineno", None)
        num_lines = (end_line - start_line + 1) if start_line and end_line else 0

        self.metadata: dict[Any, Any] = {
            "node_type": type(node).__name__,
            "has_docstring": self.has_docstring,
            "num_lines": num_lines,
        }

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

    def get_type(self) -> str:
        """Returns the AST node type (e.g., 'ClassDef', 'FunctionDef')"""
        return self.metadata["node_type"]
