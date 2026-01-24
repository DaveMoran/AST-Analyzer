"""
tests.test_analyzer

Test suite for the CodeAnalyzer class and analyzer module.
"""

import ast
from pathlib import Path
from unittest.mock import Mock

import pytest
from ast_analyzer.analyzer import CodeAnalyzer, analyzer
from ast_analyzer.ASTNode import ASTNode
from ast_analyzer.classes.AnalysisResult import AnalysisResult


def parse_code(code):
    """Parse code string and wrap in ASTNode."""
    return ASTNode(ast.parse(code))


# =============================================================================
# Helper to create mock filename
# =============================================================================
def make_filename(name="test.py"):
    """Create a mock filename object with .name attribute."""
    mock = Mock()
    mock.name = name
    return mock


# =============================================================================
# analyzer() function tests
# =============================================================================
class TestAnalyzerFunction:
    """Tests for the standalone analyzer() function."""

    def test_analyzer_returns_string(self):
        """analyzer() returns a string."""
        result = analyzer()
        assert isinstance(result, str)

    def test_analyzer_returns_expected_value(self):
        """analyzer() returns 'analyzer'."""
        assert analyzer() == "analyzer"


# =============================================================================
# CodeAnalyzer.__init__ tests
# =============================================================================
class TestCodeAnalyzerInit:
    """Tests for CodeAnalyzer.__init__"""

    def test_init_stores_tree(self):
        """__init__ stores the tree attribute."""
        tree = parse_code("x = 1")
        analyzer = CodeAnalyzer(tree, make_filename())
        assert analyzer.tree is tree

    def test_init_stores_filename(self):
        """__init__ stores the filename from .name attribute."""
        tree = parse_code("x = 1")
        analyzer = CodeAnalyzer(tree, make_filename("myfile.py"))
        assert analyzer.filename == "myfile.py"

    def test_init_creates_default_results(self):
        """__init__ creates new AnalysisResult when none provided."""
        tree = parse_code("x = 1")
        analyzer = CodeAnalyzer(tree, make_filename())
        assert isinstance(analyzer.results, AnalysisResult)
        assert len(analyzer.results) == 0

    def test_init_uses_provided_results(self):
        """__init__ uses provided AnalysisResult."""
        tree = parse_code("x = 1")
        results = AnalysisResult()
        results.append_warning("existing", "other.py")
        analyzer = CodeAnalyzer(tree, make_filename(), results=results)
        assert analyzer.results is results
        assert len(analyzer.results) == 1

    def test_init_with_path_object(self):
        """__init__ works with Path object as filename."""
        tree = parse_code("x = 1")
        path = Path("src/module.py")
        analyzer = CodeAnalyzer(tree, path)
        assert analyzer.filename == "module.py"


# =============================================================================
# CodeAnalyzer.analyze tests
# =============================================================================
class TestCodeAnalyzerAnalyze:
    """Tests for CodeAnalyzer.analyze"""

    def test_analyze_returns_results(self):
        """analyze() returns the results object."""
        tree = parse_code("x = 1")
        analyzer = CodeAnalyzer(tree, make_filename())
        result = analyzer.analyze()
        assert isinstance(result, AnalysisResult)

    def test_analyze_returns_same_results_instance(self):
        """analyze() returns the same results object passed in."""
        tree = parse_code("x = 1")
        results = AnalysisResult()
        analyzer = CodeAnalyzer(tree, make_filename(), results=results)
        returned = analyzer.analyze()
        assert returned is results

    def test_analyze_clean_code_no_findings(self):
        """analyze() produces no findings for simple clean code."""
        code = '''
"""Module docstring."""

def hello():
    """Say hello."""
    return "hello"
'''
        tree = parse_code(code)
        analyzer = CodeAnalyzer(tree, make_filename())
        results = analyzer.analyze()
        assert len(results) == 0


# =============================================================================
# CodeAnalyzer._check_function_count tests
# =============================================================================
class TestCheckFunctionCount:
    """Tests for CodeAnalyzer._check_function_count"""

    def test_no_functions_no_findings(self):
        """No findings when file has zero functions."""
        code = "x = 1"
        tree = parse_code(code)
        analyzer = CodeAnalyzer(tree, make_filename())
        analyzer._check_function_count()
        assert len(analyzer.results) == 0

    def test_four_functions_no_findings(self):
        """No findings when file has fewer than 5 functions."""
        code = """
def a(): pass
def b(): pass
def c(): pass
def d(): pass
"""
        tree = parse_code(code)
        analyzer = CodeAnalyzer(tree, make_filename())
        analyzer._check_function_count()
        assert len(analyzer.results) == 0

    def test_five_functions_warning(self):
        """Warning when file has 5 functions."""
        code = """
def a(): pass
def b(): pass
def c(): pass
def d(): pass
def e(): pass
"""
        tree = parse_code(code)
        analyzer = CodeAnalyzer(tree, make_filename())
        analyzer._check_function_count()
        assert len(analyzer.results["warnings"]) == 1
        assert len(analyzer.results["errors"]) == 0

    def test_seven_functions_warning(self):
        """Warning when file has 7 functions (between 5 and 8)."""
        code = """
def a(): pass
def b(): pass
def c(): pass
def d(): pass
def e(): pass
def f(): pass
def g(): pass
"""
        tree = parse_code(code)
        analyzer = CodeAnalyzer(tree, make_filename())
        analyzer._check_function_count()
        assert len(analyzer.results["warnings"]) == 1
        assert len(analyzer.results["errors"]) == 0

    def test_eight_functions_error(self):
        """Error when file has 8 or more functions."""
        code = """
def a(): pass
def b(): pass
def c(): pass
def d(): pass
def e(): pass
def f(): pass
def g(): pass
def h(): pass
"""
        tree = parse_code(code)
        analyzer = CodeAnalyzer(tree, make_filename())
        analyzer._check_function_count()
        assert len(analyzer.results["errors"]) == 1
        assert len(analyzer.results["warnings"]) == 0

    def test_ten_functions_error(self):
        """Error when file has 10 functions."""
        code = "\n".join([f"def func{i}(): pass" for i in range(10)])
        tree = parse_code(code)
        analyzer = CodeAnalyzer(tree, make_filename())
        analyzer._check_function_count()
        assert len(analyzer.results["errors"]) == 1


# =============================================================================
# CodeAnalyzer._check_class_count tests
# =============================================================================
class TestCheckClassCount:
    """Tests for CodeAnalyzer._check_class_count"""

    def test_no_classes_no_findings(self):
        """No findings when file has zero classes."""
        code = "x = 1"
        tree = parse_code(code)
        analyzer = CodeAnalyzer(tree, make_filename())
        analyzer._check_class_count()
        assert len(analyzer.results) == 0

    def test_four_classes_no_findings(self):
        """No findings when file has fewer than 5 classes."""
        code = """
class A: pass
class B: pass
class C: pass
class D: pass
"""
        tree = parse_code(code)
        analyzer = CodeAnalyzer(tree, make_filename())
        analyzer._check_class_count()
        assert len(analyzer.results) == 0

    def test_five_classes_warning(self):
        """Warning when file has 5 classes."""
        code = """
class A: pass
class B: pass
class C: pass
class D: pass
class E: pass
"""
        tree = parse_code(code)
        analyzer = CodeAnalyzer(tree, make_filename())
        analyzer._check_class_count()
        assert len(analyzer.results["warnings"]) == 1
        assert len(analyzer.results["errors"]) == 0

    def test_seven_classes_warning(self):
        """Warning when file has 7 classes (between 5 and 8)."""
        code = "\n".join([f"class Class{i}: pass" for i in range(7)])
        tree = parse_code(code)
        analyzer = CodeAnalyzer(tree, make_filename())
        analyzer._check_class_count()
        assert len(analyzer.results["warnings"]) == 1
        assert len(analyzer.results["errors"]) == 0

    def test_eight_classes_error(self):
        """Error when file has 8 or more classes."""
        code = "\n".join([f"class Class{i}: pass" for i in range(8)])
        tree = parse_code(code)
        analyzer = CodeAnalyzer(tree, make_filename())
        analyzer._check_class_count()
        assert len(analyzer.results["errors"]) == 1
        assert len(analyzer.results["warnings"]) == 0

    def test_ten_classes_error(self):
        """Error when file has 10 classes."""
        code = "\n".join([f"class Class{i}: pass" for i in range(10)])
        tree = parse_code(code)
        analyzer = CodeAnalyzer(tree, make_filename())
        analyzer._check_class_count()
        assert len(analyzer.results["errors"]) == 1


# =============================================================================
# CodeAnalyzer._check_function_complexity tests
# =============================================================================
class TestCheckFunctionComplexity:
    """Tests for CodeAnalyzer._check_function_complexity"""

    def test_simple_code_no_findings(self):
        """No findings for simple code with low complexity."""
        code = """
def simple():
    return 1
"""
        tree = parse_code(code)
        analyzer = CodeAnalyzer(tree, make_filename())
        analyzer._check_function_complexity()
        assert len(analyzer.results) == 0

    def test_complexity_below_10_no_findings(self):
        """No findings when complexity is below 10."""
        # 9 if statements = complexity 9
        code = """
def func():
    if a: pass
    if b: pass
    if c: pass
    if d: pass
    if e: pass
    if f: pass
    if g: pass
    if h: pass
    if i: pass
"""
        tree = parse_code(code)
        analyzer = CodeAnalyzer(tree, make_filename())
        analyzer._check_function_complexity()
        assert len(analyzer.results) == 0

    def test_complexity_10_warning(self):
        """Warning when complexity reaches 10."""
        # 10 if statements = complexity 10
        code = """
def func():
    if a: pass
    if b: pass
    if c: pass
    if d: pass
    if e: pass
    if f: pass
    if g: pass
    if h: pass
    if i: pass
    if j: pass
"""
        tree = parse_code(code)
        analyzer = CodeAnalyzer(tree, make_filename())
        analyzer._check_function_complexity()
        assert len(analyzer.results["warnings"]) == 1
        assert len(analyzer.results["errors"]) == 0

    def test_complexity_14_warning(self):
        """Warning when complexity is between 10 and 15."""
        # 14 if statements
        code = "def func():\n" + "\n".join(["    if x: pass" for _ in range(14)])
        tree = parse_code(code)
        analyzer = CodeAnalyzer(tree, make_filename())
        analyzer._check_function_complexity()
        assert len(analyzer.results["warnings"]) == 1
        assert len(analyzer.results["errors"]) == 0

    def test_complexity_15_error(self):
        """Error when complexity reaches 15."""
        # 15 if statements
        code = "def func():\n" + "\n".join(["    if x: pass" for _ in range(15)])
        tree = parse_code(code)
        analyzer = CodeAnalyzer(tree, make_filename())
        analyzer._check_function_complexity()
        assert len(analyzer.results["errors"]) == 1
        assert len(analyzer.results["warnings"]) == 0

    def test_complexity_20_error(self):
        """Error when complexity exceeds 15."""
        code = "def func():\n" + "\n".join(["    if x: pass" for _ in range(20)])
        tree = parse_code(code)
        analyzer = CodeAnalyzer(tree, make_filename())
        analyzer._check_function_complexity()
        assert len(analyzer.results["errors"]) == 1

    def test_complexity_counts_loops(self):
        """Complexity counts for and while loops."""
        code = """
def func():
    for i in range(10): pass
    for j in range(10): pass
    for k in range(10): pass
    for l in range(10): pass
    for m in range(10): pass
    while True: pass
    while True: pass
    while True: pass
    while True: pass
    while True: pass
"""
        tree = parse_code(code)
        analyzer = CodeAnalyzer(tree, make_filename())
        analyzer._check_function_complexity()
        # 10 loops should trigger warning
        assert len(analyzer.results["warnings"]) == 1

    def test_complexity_counts_except_handlers(self):
        """Complexity counts except blocks."""
        code = """
def func():
    try: pass
    except A: pass
    try: pass
    except B: pass
    try: pass
    except C: pass
    try: pass
    except D: pass
    try: pass
    except E: pass
    try: pass
    except F: pass
    try: pass
    except G: pass
    try: pass
    except H: pass
    try: pass
    except I: pass
    try: pass
    except J: pass
"""
        tree = parse_code(code)
        analyzer = CodeAnalyzer(tree, make_filename())
        analyzer._check_function_complexity()
        # 10 except blocks should trigger warning
        assert len(analyzer.results["warnings"]) == 1


# =============================================================================
# CodeAnalyzer._check_docstring_coverage tests
# =============================================================================
class TestCheckDocstringCoverage:
    """Tests for CodeAnalyzer._check_docstring_coverage"""

    def test_all_docstrings_no_findings(self):
        """No findings when module and all functions/classes have docstrings."""
        code = '''"""Module docstring."""

def func():
    """Docstring."""
    pass

class MyClass:
    """Class docstring."""
    pass
'''
        tree = parse_code(code)
        analyzer = CodeAnalyzer(tree, make_filename())
        analyzer._check_docstring_coverage()
        assert len(analyzer.results) == 0

    def test_one_missing_docstring_warning(self):
        """Warning when 1 function/class missing docstring."""
        code = """
def func():
    pass
"""
        tree = parse_code(code)
        analyzer = CodeAnalyzer(tree, make_filename())
        analyzer._check_docstring_coverage()
        assert len(analyzer.results["warnings"]) == 1
        assert len(analyzer.results["errors"]) == 0

    def test_four_missing_docstrings_warning(self):
        """Warning when 4 items missing docstrings (between 1 and 5)."""
        # 3 functions without docstrings + 1 module without docstring = 4 missing
        code = """
def a(): pass
def b(): pass
def c(): pass
"""
        tree = parse_code(code)
        analyzer = CodeAnalyzer(tree, make_filename())
        analyzer._check_docstring_coverage()
        assert len(analyzer.results["warnings"]) == 1
        assert len(analyzer.results["errors"]) == 0

    def test_five_missing_docstrings_error(self):
        """Error when 5 or more items missing docstrings."""
        code = """
def a(): pass
def b(): pass
def c(): pass
def d(): pass
def e(): pass
"""
        tree = parse_code(code)
        analyzer = CodeAnalyzer(tree, make_filename())
        analyzer._check_docstring_coverage()
        assert len(analyzer.results["errors"]) == 1
        assert len(analyzer.results["warnings"]) == 0

    def test_class_missing_docstring_counted(self):
        """Classes without docstrings are counted."""
        code = """
class A: pass
class B: pass
class C: pass
class D: pass
class E: pass
"""
        tree = parse_code(code)
        analyzer = CodeAnalyzer(tree, make_filename())
        analyzer._check_docstring_coverage()
        assert len(analyzer.results["errors"]) == 1

    def test_mixed_functions_classes_missing_docstrings(self):
        """Mixed functions and classes without docstrings counted together."""
        code = """
def a(): pass
def b(): pass
class C: pass
class D: pass
def e(): pass
"""
        tree = parse_code(code)
        analyzer = CodeAnalyzer(tree, make_filename())
        analyzer._check_docstring_coverage()
        assert len(analyzer.results["errors"]) == 1


# =============================================================================
# CodeAnalyzer._check_function_line_count tests
# =============================================================================
class TestCheckFunctionLineCount:
    """Tests for CodeAnalyzer._check_function_line_count"""

    def test_short_function_no_findings(self):
        """No findings for short functions."""
        code = """
def short():
    return 1
"""
        tree = parse_code(code)
        analyzer = CodeAnalyzer(tree, make_filename())
        analyzer._check_function_line_count()
        assert len(analyzer.results) == 0

    def test_49_lines_no_findings(self):
        """No findings when function has fewer than 50 lines."""
        # Create a function with 49 lines
        lines = ["    x = 1"] * 48
        code = "def func():\n" + "\n".join(lines)
        tree = parse_code(code)
        analyzer = CodeAnalyzer(tree, make_filename())
        analyzer._check_function_line_count()
        assert len(analyzer.results) == 0

    def test_50_lines_warning(self):
        """Warning when function has 50 lines."""
        # Create a function with 50 lines of statements
        lines = ["    x = 1"] * 50
        code = "def func():\n" + "\n".join(lines)
        tree = parse_code(code)
        analyzer = CodeAnalyzer(tree, make_filename())
        analyzer._check_function_line_count()
        assert len(analyzer.results["warnings"]) == 1
        assert len(analyzer.results["errors"]) == 0

    def test_99_lines_warning(self):
        """Warning when function has 99 lines (between 50 and 100)."""
        # 98 statement lines + 1 def line = 99 total lines
        lines = ["    x = 1"] * 98
        code = "def func():\n" + "\n".join(lines)
        tree = parse_code(code)
        analyzer = CodeAnalyzer(tree, make_filename())
        analyzer._check_function_line_count()
        assert len(analyzer.results["warnings"]) == 1
        assert len(analyzer.results["errors"]) == 0

    def test_100_lines_error(self):
        """Error when function has 100 or more lines."""
        lines = ["    x = 1"] * 100
        code = "def func():\n" + "\n".join(lines)
        tree = parse_code(code)
        analyzer = CodeAnalyzer(tree, make_filename())
        analyzer._check_function_line_count()
        assert len(analyzer.results["errors"]) == 1
        assert len(analyzer.results["warnings"]) == 0

    def test_150_lines_error(self):
        """Error when function exceeds 100 lines."""
        lines = ["    x = 1"] * 150
        code = "def func():\n" + "\n".join(lines)
        tree = parse_code(code)
        analyzer = CodeAnalyzer(tree, make_filename())
        analyzer._check_function_line_count()
        assert len(analyzer.results["errors"]) == 1


# =============================================================================
# Integration tests
# =============================================================================
class TestCodeAnalyzerIntegration:
    """Integration tests for CodeAnalyzer"""

    def test_multiple_issues_detected(self):
        """analyze() detects multiple types of issues."""
        # Code with too many functions AND missing docstrings
        code = "\n".join([f"def func{i}(): pass" for i in range(8)])
        tree = parse_code(code)
        analyzer = CodeAnalyzer(tree, make_filename())
        results = analyzer.analyze()
        # Should have error for too many functions AND error for missing docstrings
        assert len(results["errors"]) >= 2

    def test_accumulates_results_across_files(self):
        """Results accumulate when passed between analyzers."""
        code1 = """
def a(): pass
def b(): pass
def c(): pass
def d(): pass
def e(): pass
"""
        code2 = """
class A: pass
class B: pass
class C: pass
class D: pass
class E: pass
"""
        results = AnalysisResult()
        tree1 = parse_code(code1)
        analyzer1 = CodeAnalyzer(tree1, make_filename("file1.py"), results=results)
        analyzer1.analyze()

        tree2 = parse_code(code2)
        analyzer2 = CodeAnalyzer(tree2, make_filename("file2.py"), results=results)
        analyzer2.analyze()

        # Should have findings from both files
        assert len(results.results["files"]) == 2
        assert "file1.py" in results.results["files"]
        assert "file2.py" in results.results["files"]

    def test_findings_include_filename(self):
        """Findings include the correct filename."""
        code = "\n".join([f"def func{i}(): pass" for i in range(8)])
        tree = parse_code(code)
        analyzer = CodeAnalyzer(tree, make_filename("mymodule.py"))
        results = analyzer.analyze()
        # All findings should reference the filename
        for finding in results:
            assert finding["file"] == "mymodule.py"

    def test_clean_well_documented_code(self):
        """Well-structured code produces no findings."""
        code = '''
"""Module with good practices."""

def helper():
    """A simple helper function."""
    return 42

class Calculator:
    """A simple calculator class."""

    def add(self, a, b):
        """Add two numbers."""
        return a + b

    def subtract(self, a, b):
        """Subtract b from a."""
        return a - b
'''
        tree = parse_code(code)
        analyzer = CodeAnalyzer(tree, make_filename())
        results = analyzer.analyze()
        assert len(results) == 0
        assert not results  # Falsy when empty
