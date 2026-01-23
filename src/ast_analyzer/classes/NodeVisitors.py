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


class ClassCounter(ASTNodeVisitor):
    """Counts ClassDef nodes using ASTNode trees."""

    def __init__(self):
        self.count = 0

    def __str__(self):
        return f"Number of classes: {self.count}"

    def visit_ClassDef(self, node):
        """Called when a function call (ast.Call node) is encountered."""
        self.count += 1
        # Continue visiting child nodes to find nested calls, arguments, etc.
        self.generic_visit(node)


class HasDocstring(ASTNodeVisitor):
    """Checks if FunctionDef, AsyncFunctionDef, ClassDef, and Module nodes contain docstrings using ASTNode trees."""

    def __init__(self):
        self.has_docstring = False

    def __bool__(self):
        return self.has_docstring

    def __str__(self):
        return f"Number of functions: {self.count}"

    def visit_FunctionDef(self, node):
        """Called when a function call (ast.Call node) is encountered."""
        if node.metadata["has_docstring"]:
            self.has_docstring = True

    def visit_AsyncFunctionDef(self, node):
        """Called when an async function call (ast.Call node) is encountered."""
        if node.metadata["has_docstring"]:
            self.has_docstring = True

    def visit_ClassDef(self, node):
        """Called when a class call (ast.Call node) is encountered."""
        if node.metadata["has_docstring"]:
            self.has_docstring = True

    def visit_Module(self, node):
        """Called when a module call (ast.Call node) is encountered."""
        if node.metadata["has_docstring"]:
            self.has_docstring = True
