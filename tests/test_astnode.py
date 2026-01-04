import ast
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
        test_tree = ast.parse(test_code)
        self.node = ASTNode(test_tree)
        return

    def test_len(self):
        """TODO - Ensure that the pythonic len function works"""

        return

    def test_getitem(self):
        """TODO - Ensure that index retrieval works"""
        return

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
