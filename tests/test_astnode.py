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
        return

    def test_len(self):
        """TODO - Ensure that the pythonic len function works"""
        assert len(self.node) == 2
