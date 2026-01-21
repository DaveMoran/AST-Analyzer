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


@pytest.mark.astnode
class TestASTNodeLen:
    """Tests for ASTNode.__len__"""

    def test_len_empty_module(self, empty_ast_node):
        """Empty module has zero children."""
        assert len(empty_ast_node) == 0

    def test_len_single_child(self, ast_node):
        """Simple assignment has one child."""
        assert len(ast_node) == 1

    def test_len_multiple_children(self, complex_ast_node):
        """Complex module has multiple children."""
        # def greet, class Calculator, x = 1, y = 2
        assert len(complex_ast_node) == 2


@pytest.mark.astnode
class TestASTNodeGetitem:
    """Tests for ASTNode.__getitem__"""

    def test_getitem_valid_index(self, ast_node):
        """Valid index returns the child ASTNode."""
        child = ast_node[0]
        assert isinstance(child, ASTNode)

    def test_getitem_negative_index(self, complex_ast_node):
        """Negative index returns from end."""
        last_child = complex_ast_node[-1]
        assert last_child is complex_ast_node.children[-1]

    def test_getitem_index_error(self, ast_node):
        """Out of range index raises IndexError."""
        with pytest.raises(IndexError):
            _ = ast_node[100]

    def test_getitem_empty_node_raises(self, empty_ast_node):
        """Indexing empty node raises IndexError."""
        with pytest.raises(IndexError):
            _ = empty_ast_node[0]


@pytest.mark.astnode
class TestASTNodeIter:
    """Tests for ASTNode.__iter__"""

    def test_iter_yields_children(self, complex_ast_node):
        """Iterating yields all children in order."""
        children_via_iter = list(complex_ast_node)
        assert children_via_iter == complex_ast_node.children

    def test_iter_empty_node(self, empty_ast_node):
        """Iterating empty node yields nothing."""
        children = list(empty_ast_node)
        assert children == []

    def test_iter_in_for_loop(self, ast_node):
        """Can use ASTNode in for loop."""
        count = 0
        for child in ast_node:
            assert isinstance(child, ASTNode)
            count += 1
        assert count == len(ast_node)
