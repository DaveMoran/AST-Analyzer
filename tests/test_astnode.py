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
        with self.assertRaises(IndexError):
            self.node[3]

    def test_repr(self):
        """TODO - Ensure that repr returns debugging information"""
        return

    def test_str(self):
        """TODO - Ensure that str returns a user friendly string"""
        return

    def test_hash(self):
        """TODO - Ensure that ASTNodes can be added to sets/dics"""
        return

    def test_iter(self):
        """TODO - Ensure for loops can iterate over node children"""
        return
