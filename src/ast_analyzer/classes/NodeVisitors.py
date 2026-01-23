"""
Group of classes that maintain all of the Node Visitors we'll be using for our
AST Analyzer
"""

from ast_analyzer.ASTNode import ASTNodeVisitor


class FunctionCounter(ASTNodeVisitor):
    """Counts FunctionDef and AsyncFunctionDef nodes using ASTNode trees."""

    def __init__(self):
        self.count = 0

    def __str__(self):
        return f"Number of functions: {self.count}"

    def visit_FunctionDef(self, node):
        """Called when a function call (ast.Call node) is encountered."""
        self.count += 1
        # Continue visiting child nodes to find nested calls, arguments, etc.
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        """Called when a function call (ast.Call node) is encountered."""
        self.count += 1
        # Continue visiting child nodes to find nested calls, arguments, etc.
        self.generic_visit(node)
