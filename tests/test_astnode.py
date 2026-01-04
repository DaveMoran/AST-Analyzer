import ast
import textwrap
import unittest
from ast_analyzer.ASTNode import ASTNode


class TestASTNode(unittest.TestCase):

    def setUp(self):
        """TODO - hook method for setting up fixtures before each test method is called"""
        test_code = """
        def greet_user(message, name):
            intro = f"Hello, {name}! We have a special message for you"
            return f"{intro}. {message}"

        greet_user("Happy New Year!", "Dave")
        """
        dedented_code = textwrap.dedent(test_code)
        test_tree = ast.parse(dedented_code)
        self.node = ASTNode(test_tree)

    def test_len(self):
        """TODO - Ensure that the pythonic len function works"""
        assert len(self.node) == 2

    def test_getitem(self):
        assert isinstance(self.node[0], ASTNode)
        assert isinstance(self.node[0].node, ast.FunctionDef)
        with self.assertRaises(IndexError):
            self.node[3]

    def test_repr(self):
        repr_str = repr(self.node)
        assert repr_str == "ASTNode(Module)"

    def test_str(self):
        repr_str = str(self.node)
        assert repr_str == "AST Node | Children: 2"

    def test_hash(self):
        test_set = set()
        test_set.add(self.node)
        assert len(test_set) == 1

    def test_iter(self):
        for node in self.node:
            assert str(node).startswith("AST Node")
            assert repr(node).startswith("ASTNode")
