"""
tests.test_parser
"""

import tempfile
import os

from ast_analyzer.parser import Parser


class TestParserContextManager:
    """Test the Parser context manager functionality"""

    def test_parser_opens_and_closes_file(self):
        """Test that Parser properly opens and closes a file"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as tmp:
            tmp.write("print('hello')")
            tmp_path = tmp.name

        try:
            with Parser(tmp_path) as f:
                content = f.read()
                assert content == "print('hello')"
        finally:
            os.unlink(tmp_path)

    def test_parser_file_closed_after_exit(self):
        """Test that file is closed after exiting context"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as tmp:
            tmp.write("x = 1")
            tmp_path = tmp.name

        try:
            parser = Parser(tmp_path)
            with parser as f:
                pass
            assert parser.file.closed
        finally:
            os.unlink(tmp_path)

    def test_parser_file_closed_on_exception(self):
        """Test that file is closed even when an exception occurs inside the block"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as tmp:
            tmp.write("x = 1")
            tmp_path = tmp.name

        try:
            parser = Parser(tmp_path)
            try:
                with parser as f:
                    raise ValueError("Test exception")
            except ValueError:
                pass
            assert parser.file.closed
        finally:
            os.unlink(tmp_path)

    def test_parser_file_not_found_raises_exception(self):
        """Test that FileNotFoundError is raised for non-existent files"""
        try:
            with Parser("/nonexistent/path/file.py") as f:
                content = f.read()
            assert False, "Should have raised FileNotFoundError"
        except FileNotFoundError:
            pass

    def test_parser_reads_multiline_content(self):
        """Test that Parser can read multiline file content"""
        code = """def hello():
    print('world')

class Foo:
    pass
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as tmp:
            tmp.write(code)
            tmp_path = tmp.name

        try:
            with Parser(tmp_path) as f:
                content = f.read()
                assert "def hello():" in content
                assert "class Foo:" in content
        finally:
            os.unlink(tmp_path)
