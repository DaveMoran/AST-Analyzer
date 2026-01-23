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

    def __init__(
        self,
        tree,
        filename,
        results=None,
    ):
        self.tree = tree
        self.results = results if results is not None else AnalysisResult()
        self.filename = filename.name

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

        If >= 10, add to warnings list.
        If >= 15, add to errors list.
        """
        print("TODO: _check_function_complexity")
        pass

    def _check_function_count(self):
        """
        Uses a visitor to traverse the FunctionDef to see how many times the
        function is called.

        If count >= 5, add a warning
        If count >= 8, add an error
        """
        num_funcs = 0
        for node in self.tree:
            if node.get_type() == "FunctionDef":
                num_funcs += 1

        if num_funcs >= 8:
            self.results.append_error(f"Too many functions ({num_funcs}).", self.filename)
        elif num_funcs >= 5:
            self.results.append_warning(f"This file has ({num_funcs}) functions.", self.filename)

    def _check_class_count(self):
        """
        Takes a Module and counts how many ClassDef are inside

        If >= 5, add to warnings list.
        If >= 8, add to errors list.
        """
        num_classes = 0
        for node in self.tree:
            if node.get_type() == "ClassDef":
                num_classes += 1

        if num_classes >= 8:
            self.results.append_error(f"Too many classes ({num_classes}).", self.filename)
        elif num_classes >= 5:
            self.results.append_warning(f"This file has ({num_classes}) classes.", self.filename)

    def _check_docstring_coverage(self):
        """
        Use ast's built in get_docstring to see how many FunctionDef and
        ClassDef nodes contain a docstring

        If >= 1, add to warnings list.
        If >= 5, add to errors list.
        """
        counter = 0
        for node in self.tree:
            if node.get_type() in [
                "FunctionDef",
                "AsyncFunctionDef",
                "ClassDef",
                "Module",
            ]:
                if not node.metadata["has_docstring"]:
                    counter += 1

        if counter >= 5:
            self.results.append_error(
                f"Too many items without docstring ({counter})", self.filename
            )
        elif counter >= 1:
            self.results.append_warning(f"Missing {counter} docstrings", self.filename)

    def _check_unused_imports(self):
        """
        Check list of imports and see if they are called in any FunctionDef
        nodes

        If >= 1, add to warnings list.
        If >= 3, add to errors list.
        """
        print("TODO: _check_unused_imports")
        pass

    def _check_circular_imports(self):
        """
        TODO: Research how to check for circular imports
        """
        print("TODO: _check_circular_imports")
        pass

    def _check_function_line_count(self):
        """
        Takes a FunctionDef node and checks the lineno property to see how many
        lines the function has.

        If >= 50, add to warnings list.
        If >= 100, add to errors list.
        """
        for node in self.tree:
            if node.get_type() == "FunctionDef":
                num_lines = node.metadata["num_lines"]

                if num_lines >= 100:
                    self.results.append_error(
                        f"Function too large ({num_lines} lines)", self.filename
                    )
                elif num_lines >= 50:
                    self.results.append_warning(
                        f"Function starting to grow unweildy ({num_lines})",
                        self.filename,
                    )

    def _check_nesting_depth(self):
        """
        Checks for depth of FunctionDef and ClassDef to see how many
        loops/conditionals are included in the function.

        If >= 10, add to warnings list.
        If >= 15, add to errors list.
        """
        print("TODO: _check_nesting_depth")
        pass

    def _check_naming_conventions(self):
        """
        Checks the name of each ClassDef, FunctionDef, and Assign targets to
        make sure that they are following proper conventions

        If >= 10, add to warnings list.
        If >= 15, add to errors list.
        """
        print("TODO: _check_naming_conventions")
        pass
