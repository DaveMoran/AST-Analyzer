"""Shared pytest fixtures for AST Analyzer tests."""

import ast
import pytest
from ast_analyzer.ASTNode import ASTNode


@pytest.fixture
def simple_ast_tree():
    """Parse a simple assignment statement into an AST."""
    return ast.parse("x = 1")


@pytest.fixture
def complex_ast_tree():
    """Parse a complex module with functions and classes."""
    code = """
def greet_user(message, name):
    intro = f"Hello, {name}! We have a special message for you"
    return f"{intro}. {message}"

greet_user("Happy New Year!", "Dave")
"""
    return ast.parse(code)


@pytest.fixture
def empty_ast_tree():
    """Parse an empty module."""
    return ast.parse("")


@pytest.fixture
def function_ast_tree():
    """Parse a simple function definition."""
    return ast.parse("def foo(): pass")


# -----------------------------------------------------------------------------
# ASTNode Fixtures
# -----------------------------------------------------------------------------
@pytest.fixture
def ast_node(simple_ast_tree):
    """Create an ASTNode from a simple AST tree."""
    return ASTNode(simple_ast_tree)


@pytest.fixture
def complex_ast_node(complex_ast_tree):
    """Create an ASTNode from a complex AST tree with nested children."""
    return ASTNode(complex_ast_tree)


@pytest.fixture
def empty_ast_node(empty_ast_tree):
    """Create an ASTNode from an empty module (no children)."""
    return ASTNode(empty_ast_tree)


@pytest.fixture
def function_ast_node(function_ast_tree):
    """Create an ASTNode wrapping a function definition."""
    return ASTNode(function_ast_tree)
