"""
ast_analyzer.reporter

Take the analysis of the project and generate a user friendly report to be displayed along with suggestions
on how to improve said project
"""


def reporter():
    return "reporter"


class MetricsCollector:
    """
    Use built-in functionality of black, ruff, and mypy to generate additional
    reports based on standard practices
    """

    def __init__(self):
        self.total_fns = 0
        self.total_lines = 0
        self.files_analyzed = 0

    def add_file_metrics(self, fn_count, ln_count):
        self.total_fns += fn_count
        self.total_lines += ln_count
        self.files_analyzed += 1

    def get_summary(self):
        return {
            "files": self.files_analyzed,
            "functions": self.total_fns,
            "avg_fns_per_file": self.total_fns / self.files_analyzed,
        }
