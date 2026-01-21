import ast
import pytest
from ast_analyzer.ASTNode import ASTNode


@pytest.mark.astnode
class TestASTNodeInit:
    """Tests for ASTNode.__init__"""

    def test_init_creates_node(self, simple_ast_tree):
        """ASTNode wraps the provided AST node."""
        node = ASTNode(simple_ast_tree)
        assert node.node is simple_ast_tree

    def test_init_parent_default_none(self, simple_ast_tree):
        """Parent defaults to None for root nodes."""
        node = ASTNode(simple_ast_tree)
        assert node.parent is None

    def test_init_parent_assignment(self, simple_ast_tree):
        """Parent can be explicitly set."""
        parent = ASTNode(simple_ast_tree)
        child_ast = ast.parse("y = 2")
        child = ASTNode(child_ast, parent=parent)
        assert child.parent is parent

    def test_init_creates_children_recursively(self, simple_ast_tree):
        """Children are created for all child AST nodes."""
        node = ASTNode(simple_ast_tree)
        # simple_ast_tree is "x = 1" which has one Assign child
        assert len(node.children) == 1
        assert isinstance(node.children[0], ASTNode)

    def test_init_children_have_parent_set(self, simple_ast_tree):
        """All children have their parent reference set correctly."""
        node = ASTNode(simple_ast_tree)
        for child in node.children:
            assert child.parent is node

    def test_init_metadata_empty_dict(self, simple_ast_tree):
        """Metadata initializes as empty dict."""
        node = ASTNode(simple_ast_tree)
        assert node.metadata == {}
        assert isinstance(node.metadata, dict)
