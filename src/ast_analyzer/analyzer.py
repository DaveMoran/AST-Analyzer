"""
ast_analyzer.analyzer

Responsible for going through the parsed files and determining what updates should be made based on a predetermined
criteria of suggestions
"""

from ast_analyzer.classes.AnalysisResult import AnalysisResult


def analyzer():
    return "analyzer"


class CodeAnalyzer:
    """
    Analyze parsed code via AST to generate findings from custom linting and
    errors found during tree traversal

    Parameters:
    -----------
      tree: The parsed AST Tree that the analyzer will be navagating through
    """

    def __init__(self, tree):
        self.tree = tree
        self.results = AnalysisResult()

    def analyze(self):
        """
        Runs all helper methods to populate our results. Once populated, it will
        return the findings populated in the self.results variable
        """
        self._check_function_complexity()
        self._check_function_count()
        self._check_class_count()
        self._check_docstring_coverage()
        self._check_unused_imports()
        self._check_circular_imports()
        self._check_function_line_count()
        self._check_nesting_depth()
        self._check_naming_conventions()
        return self.results

    def _check_function_complexity(self):
        """
        Use a custom rubric to determine the complexity of the code. Combines
        findings from the existing result scan as well as other best practices
        """
        pass

    def _check_function_count(self):
        """
        Uses a visitor to traverse the FunctionDef to see how many times the
        function is called.

        If count > 5, add an error
        If count > 3, add a warning
        """
        pass

    def _check_class_count(self):
        pass

    def _check_docstring_coverage(self):
        pass

    def _check_unused_imports(self):
        pass

    def _check_circular_imports(self):
        pass

    def _check_function_line_count(self):
        """
        Takes a FunctionDef node and checks the lineno property to see how many
        lines the function has.
        If >= 50, add to warnings list.
        If >= 100, add to errors list.
        """
        pass

    def _check_nesting_depth(self):
        pass

    def _check_naming_conventions(self):
        pass
