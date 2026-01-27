"""
Group of classes that maintain all of the Node Visitors we'll be using for our
AST Analyzer
"""

import ast

from ast_analyzer import ASTNode


class FunctionCounter(ASTNode.ASTNodeVisitor):
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


class ClassCounter(ASTNode.ASTNodeVisitor):
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


class MissingDocstringCounter(ASTNode.ASTNodeVisitor):
    """Checks if FunctionDef, AsyncFunctionDef, ClassDef, and Module nodes contain docstrings using ASTNode trees."""

    def __init__(self):
        self.count = 0

    def __bool__(self):
        return self.count > 0

    def __str__(self):
        return f"Node is missing {self.count} docstrings"

    def visit_FunctionDef(self, node):
        """Called when a FunctionDef node is encountered."""
        if not ast.get_docstring(node.node):
            self.count += 1
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        """Called when an AsyncFunctionDef node is encountered."""
        if not ast.get_docstring(node.node):
            self.count += 1
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        """Called when a ClassDef node is encountered."""
        if not ast.get_docstring(node.node):
            self.count += 1
        self.generic_visit(node)

    def visit_Module(self, node):
        """Called when a Module node is encountered."""
        if not ast.get_docstring(node.node):
            self.count += 1
        self.generic_visit(node)


class FunctionLineCounter(ASTNode.ASTNodeVisitor):
    """Counts FunctionDef and AsyncFunctionDef nodes using ASTNode trees."""

    def __init__(self):
        self.num_lines = 0

    def __str__(self):
        return f"Number of lines in function: {self.num_lines}"

    def visit_FunctionDef(self, node):
        """Called when a function call (ast.Call node) is encountered."""
        start_line = getattr(node.node, "lineno", None)
        end_line = getattr(node.node, "end_lineno", None)
        num_lines = (end_line - start_line + 1) if start_line and end_line else 0

        self.num_lines = num_lines
        # Continue visiting child nodes to find nested calls, arguments, etc.
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        """Called when an async function call (ast.Call node) is encountered."""
        start_line = getattr(node.node, "lineno", None)
        end_line = getattr(node.node, "end_lineno", None)
        num_lines = (end_line - start_line + 1) if start_line and end_line else 0

        self.num_lines = num_lines
        # Continue visiting child nodes to find nested calls, arguments, etc.
        self.generic_visit(node)


class ComplexityCounter(ASTNode.ASTNodeVisitor):
    """
    Calculates complexity score for functions based on:
    - Branches: if, elif, ternary expressions (+1 each)
    - Loops: for, while, comprehensions (+1 each)
    - Exception handlers: except blocks (+1 each)
    """

    def __init__(self):
        self.score = 0

    def __str__(self):
        return f"Complexity score: {self.score}"

    # Branches
    def visit_If(self, node):
        """Count if/elif statements."""
        self.score += 1
        self.generic_visit(node)

    def visit_IfExp(self, node):
        """Count ternary expressions (x if cond else y)."""
        self.score += 1
        self.generic_visit(node)

    # Loops
    def visit_For(self, node):
        """Count for loops."""
        self.score += 1
        self.generic_visit(node)

    def visit_While(self, node):
        """Count while loops."""
        self.score += 1
        self.generic_visit(node)

    def visit_ListComp(self, node):
        """Count list comprehensions."""
        self.score += 1
        self.generic_visit(node)

    def visit_SetComp(self, node):
        """Count set comprehensions."""
        self.score += 1
        self.generic_visit(node)

    def visit_DictComp(self, node):
        """Count dict comprehensions."""
        self.score += 1
        self.generic_visit(node)

    def visit_GeneratorExp(self, node):
        """Count generator expressions."""
        self.score += 1
        self.generic_visit(node)

    # Exception handlers
    def visit_ExceptHandler(self, node):
        """Count except blocks."""
        self.score += 1
        self.generic_visit(node)
