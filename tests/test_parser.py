"""
tests.test_parser
"""

import ast
import os

import pytest

from ast_analyzer.parser import Parser


@pytest.fixture
def temp_python_file(tmp_path):
    """Fixture that creates a temporary Python file"""

    def _create_file(content: str, suffix: str = ".py") -> str:
        file_path = tmp_path / f"test{suffix}"
        file_path.write_text(content)
        return str(file_path)

    return _create_file


class TestParserContextManager:
    """Test the Parser context manager functionality"""

    def test_parser_enter_returns_file_object(self, temp_python_file):
        """Test that __enter__ returns the file object"""
        path = temp_python_file("x = 1")
        with Parser(path) as f:
            assert hasattr(f, "read")
            assert hasattr(f, "readline")

    def test_parser_opens_and_closes_file(self, temp_python_file):
        """Test that Parser properly opens and closes a file"""
        path = temp_python_file("print('hello')")
        with Parser(path) as f:
            content = f.read()
            assert content == "print('hello')"

    def test_parser_file_closed_after_exit(self, temp_python_file):
        """Test that file is closed after exiting context"""
        path = temp_python_file("x = 1")
        parser = Parser(path)
        with parser:
            pass
        assert parser.file.closed

    def test_parser_file_closed_on_exception(self, temp_python_file):
        """Test that file is closed even when an exception occurs inside the block"""
        path = temp_python_file("x = 1")
        parser = Parser(path)
        with pytest.raises(ValueError):
            with parser:
                raise ValueError("Test exception")
        assert parser.file.closed

    def test_parser_reuse_raises_error(self, temp_python_file):
        """Test that reusing same Parser instance fails after file is closed"""
        path = temp_python_file("x = 1")
        parser = Parser(path)
        with parser:
            pass
        with pytest.raises(ValueError):
            with parser:
                pass


class TestParserErrorHandling:
    """Test Parser error conditions"""

    def test_parser_file_not_found_raises_exception(self):
        """Test that FileNotFoundError is raised for non-existent files"""
        with pytest.raises(FileNotFoundError):
            with Parser("/nonexistent/path/file.py"):
                pass

    def test_parser_permission_denied(self, temp_python_file):
        """Test that PermissionError is raised for unreadable files"""
        path = temp_python_file("x = 1")
        os.chmod(path, 0o000)
        try:
            with pytest.raises(PermissionError):
                with Parser(path):
                    pass
        finally:
            os.chmod(path, 0o644)

    def test_parser_directory_path_raises_error(self):
        """Test that IsADirectoryError is raised when given a directory"""
        with pytest.raises(IsADirectoryError):
            with Parser("/tmp"):
                pass

    def test_parser_empty_file(self, temp_python_file):
        """Test that Parser handles empty files correctly"""
        path = temp_python_file("")
        with Parser(path) as f:
            content = f.read()
            assert content == ""


class TestParserFileReading:
    """Test Parser file reading capabilities"""

    def test_parser_reads_multiline_content(self, temp_python_file):
        """Test that Parser can read multiline file content"""
        code = """def hello():
    print('world')

class Foo:
    pass
"""
        path = temp_python_file(code)
        with Parser(path) as f:
            content = f.read()
            assert "def hello():" in content
            assert "class Foo:" in content

    def test_parser_handles_utf8_encoding(self, temp_python_file):
        """Test that Parser handles UTF-8 encoded files"""
        code = "# Comment with émojis 🎉 and spëcial characters"
        path = temp_python_file(code)
        with Parser(path) as f:
            content = f.read()
            assert "émojis" in content
            assert "🎉" in content


class TestParserASTIntegration:
    """Test Parser integration with AST parsing"""

    def test_parser_content_can_be_parsed_to_ast(self, temp_python_file):
        """Test that content read by Parser can be parsed into AST"""
        code = """def greet(name):
    return f"Hello, {name}"
"""
        path = temp_python_file(code)
        with Parser(path) as f:
            content = f.read()
            tree = ast.parse(content)
            assert isinstance(tree, ast.Module)
            assert len(tree.body) == 1
            assert isinstance(tree.body[0], ast.FunctionDef)

    def test_parser_invalid_python_syntax(self, temp_python_file):
        """Test that invalid Python syntax raises SyntaxError during ast.parse"""
        code = "def broken(:\n    pass"
        path = temp_python_file(code)
        with Parser(path) as f:
            content = f.read()
            with pytest.raises(SyntaxError):
                ast.parse(content)


@pytest.mark.parser
class TestParserEnter:
    """Tests for Parser.__enter__"""

    def test_enter_opens_file(self, sample_code_file):
        """__enter__ opens the file and returns file object."""
        filepath = sample_code_file("x = 1")
        with Parser(filepath) as f:
            assert f is not None
            assert not f.closed

    def test_enter_file_readable(self, sample_code_file):
        """Opened file can be read."""
        filepath = sample_code_file("x = 1\ny = 2")
        with Parser(filepath) as f:
            content = f.read()
            assert "x = 1" in content


@pytest.mark.parser
class TestParserExit:
    """Tests for Parser.__exit__"""

    def test_exit_closes_file(self, sample_code_file):
        """__exit__ closes the file."""
        filepath = sample_code_file("test content")
        parser = Parser(filepath)
        f = parser.__enter__()
        assert not f.closed
        parser.__exit__(None, None, None)
        assert f.closed

    def test_exit_returns_false(self, sample_code_file):
        """__exit__ returns False (doesn't suppress exceptions)."""
        filepath = sample_code_file("test")
        parser = Parser(filepath)
        parser.__enter__()
        result = parser.__exit__(None, None, None)
        assert result is False

    def test_exit_with_exception(self, sample_code_file):
        """__exit__ handles exceptions and still closes file."""
        filepath = sample_code_file("test")
        parser = Parser(filepath)
        f = parser.__enter__()
        # Simulate an exception occurring
        result = parser.__exit__(ValueError, ValueError("test error"), None)
        assert f.closed
        assert result is False  # Exception not suppressed


@pytest.mark.parser
class TestParserContextManager:
    """Integration tests for Parser as context manager."""

    def test_context_manager_usage(self, sample_code_file):
        """Parser works correctly as context manager."""
        filepath = sample_code_file("print('hello')")
        file_ref = None
        with Parser(filepath) as f:
            file_ref = f
            assert not f.closed
        assert file_ref.closed

    def test_context_manager_with_exception(self, sample_code_file):
        """File is closed even when exception occurs."""
        filepath = sample_code_file("content")
        file_ref = None
        with pytest.raises(ValueError):
            with Parser(filepath) as f:
                file_ref = f
                raise ValueError("test error")
        assert file_ref.closed

    def test_nonexistent_file_raises(self, tmp_path):
        """Opening nonexistent file raises FileNotFoundError."""
        nonexistent = str(tmp_path / "does_not_exist.py")
        with pytest.raises(FileNotFoundError):
            with Parser(nonexistent) as f:
                pass
