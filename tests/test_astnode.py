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


@pytest.mark.astnode
class TestASTNodeRepr:
    """Tests for ASTNode.__repr__"""

    @pytest.mark.parametrize(
        "code,expected_type",
        [
            ("x = 1", "Module"),
            ("def foo(): pass", "Module"),
            ("class Bar: pass", "Module"),
        ],
    )
    def test_repr_format(self, code, expected_type):
        """__repr__ returns ASTNode({node_type})."""
        tree = ast.parse(code)
        node = ASTNode(tree)
        assert repr(node) == f"ASTNode({expected_type})"

    def test_repr_child_node_type(self, simple_ast_tree):
        """Child nodes show their specific type."""
        node = ASTNode(simple_ast_tree)
        child = node.children[0]
        assert repr(child) == "ASTNode(Assign)"


@pytest.mark.astnode
class TestASTNodeStr:
    """Tests for ASTNode.__str__"""

    @pytest.mark.parametrize(
        "code,expected_count",
        [
            ("", 0),
            ("x = 1", 1),
            ("x = 1\ny = 2", 2),
            ("x = 1\ny = 2\nz = 3", 3),
        ],
    )
    def test_str_shows_children_count(self, code, expected_count):
        """__str__ displays the number of children."""
        tree = ast.parse(code)
        node = ASTNode(tree)
        assert str(node) == f"AST Node | Children: {expected_count}"
